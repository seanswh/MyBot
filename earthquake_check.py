#!/usr/bin/env python3
"""
地震检查脚本 - 每10分钟检查Wolfx.jp地震API
"""

import json
import requests
import datetime
import os
from pathlib import Path

# 配置文件路径
STATE_FILE = Path(__file__).parent / "earthquake_state.json"
API_URL = "https://api.wolfx.jp/cenc_eqlist.json"

def load_state():
    """加载状态文件"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "lastEventId": "",
        "lastCheckTime": "",
        "lastEarthquakeTime": ""
    }

def save_state(state):
    """保存状态文件"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def fetch_earthquake_data():
    """获取地震数据"""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取地震数据失败: {e}")
        return None

def find_new_earthquakes(data, last_event_id):
    """找出新地震事件"""
    new_events = []
    
    # 按No1, No2...顺序检查（No1是最新的）
    for i in range(1, 51):
        key = f"No{i}"
        if key not in data:
            break
            
        event = data[key]
        event_id = event.get("EventID")
        
        # 如果找到上次的地震ID，停止检查
        if event_id == last_event_id:
            break
            
        # 记录新地震
        new_events.append(event)
    
    # 反转列表，让最早的地震在前
    return list(reversed(new_events))

def format_earthquake_message(event):
    """格式化地震信息为可读消息"""
    return (
        f"🌍 新地震报告 🌍\n"
        f"📍 地点: {event.get('location', '未知')}\n"
        f"⏰ 时间: {event.get('time', '未知')}\n"
        f"📊 震级: {event.get('magnitude', '未知')}级\n"
        f"📏 深度: {event.get('depth', '未知')}公里\n"
        f"💥 烈度: {event.get('intensity', '未知')}级\n"
        f"🆔 事件ID: {event.get('EventID', '未知')}\n"
        f"🔗 数据来源: Wolfx.jp"
    )

def main():
    print(f"[{datetime.datetime.now().isoformat()}] 开始检查地震数据...")
    
    # 加载上次状态
    state = load_state()
    last_event_id = state.get("lastEventId", "")
    print(f"上次记录的地震ID: {last_event_id or '无'}")
    
    # 获取地震数据
    data = fetch_earthquake_data()
    if not data:
        return
    
    # 检查最新地震ID
    latest_event = data.get("No1")
    if not latest_event:
        print("未找到地震数据")
        return
        
    latest_event_id = latest_event.get("EventID")
    latest_time = latest_event.get("time")
    
    print(f"最新地震ID: {latest_event_id}")
    print(f"最新地震时间: {latest_time}")
    
    # 如果没有上次记录，只保存状态不发送通知
    if not last_event_id:
        print("首次运行，只保存状态不发送通知")
        state["lastEventId"] = latest_event_id
        state["lastEarthquakeTime"] = latest_time
        state["lastCheckTime"] = datetime.datetime.now().isoformat()
        save_state(state)
        return
    
    # 检查是否有新地震
    if latest_event_id == last_event_id:
        print("没有新地震")
        # 更新检查时间
        state["lastCheckTime"] = datetime.datetime.now().isoformat()
        save_state(state)
        return
    
    print(f"发现新地震！最新ID: {latest_event_id}")
    
    # 找出所有新地震
    new_events = find_new_earthquakes(data, last_event_id)
    print(f"发现 {len(new_events)} 个新地震事件")
    
    # 准备发送消息
    if new_events:
        messages = []
        for event in new_events:
            messages.append(format_earthquake_message(event))
        
        # 保存状态
        state["lastEventId"] = latest_event_id
        state["lastEarthquakeTime"] = latest_time
        state["lastCheckTime"] = datetime.datetime.now().isoformat()
        save_state(state)
        
        # 返回消息（将由OpenClaw发送）
        for msg in messages:
            print("--- 新地震消息 ---")
            print(msg)
            print("---")
        
        return messages
    
    # 如果没找到新事件但ID变了（可能是数据更新问题）
    state["lastEventId"] = latest_event_id
    state["lastEarthquakeTime"] = latest_time
    state["lastCheckTime"] = datetime.datetime.now().isoformat()
    save_state(state)
    print("更新了地震ID但未发现新事件")

if __name__ == "__main__":
    main()