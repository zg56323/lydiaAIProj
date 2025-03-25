import json
import requests
import streamlit as st


def call_workflow_with_input(user_input, api_key, response_mode="blocking"):
    """
    根据用户输入生成请求参数并发送 POST 请求

    :param api_key:
    :param user_input: 用户输入的消息
    :param response_mode: 响应模式 (streaming/blocking)
    :return:
      - blocking 模式返回处理后的输出内容
      - streaming 模式返回事件生成器
    """
    # 公共请求参数配置
    url = "http://192.168.2.10/v1/workflows/run"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {"input": user_input},
        "response_mode": response_mode,
        "user": f"{st.session_state['user']}"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            stream=(response_mode == "streaming")
        )

        if response.status_code != 200:
            raise Exception(f"请求失败，状态码: {response.status_code}, 响应内容: {response.text}")

        # 路由到不同的响应处理器
        if response_mode == "blocking":
            return _handle_blocking_response(response)
        elif response_mode == "streaming":
            return _handle_streaming_response(response)

    except requests.exceptions.RequestException as e:
        raise Exception(f"请求异常: {e}")


def _handle_blocking_response(response):
    """处理阻塞式响应"""
    response_data = response.json()
    outputs = response_data["data"]["outputs"]

    # 清理和转换输出
    cleaned_outputs = {
        k: v.strip().replace('\n\n', '\n')
        for k, v in outputs.items()
        if v not in (None, "", "null")
    }

    # 智能字段选择
    priority_fields = ['output1', 'text', 'result']
    for field in priority_fields:
        if field in cleaned_outputs:
            return cleaned_outputs[field]

    # 兜底返回所有有效字段
    return "\n".join(
        f"{k}: {v}"
        for k, v in cleaned_outputs.items()
        if v
    )


def _handle_streaming_response(response):
    """处理流式响应"""

    def event_generator():
        buffer = ""
        current_status = {
            'workflow_id': None,
            'task_id': None,
            'current_node': None,
            'outputs': {}
        }

        for chunk in response.iter_content(chunk_size=1024):
            if not chunk:
                continue

            buffer += chunk.decode('utf-8')
            while "\n\n" in buffer:
                event, buffer = buffer.split("\n\n", 1)
                if not event.startswith("data: "):
                    continue

                try:
                    event_data = json.loads(event[6:])  # 移除 data: 前缀
                    processed = _process_stream_event(event_data, current_status)
                    yield processed

                    # 遇到最终事件时终止流
                    if event_data.get("event") == "workflow_finished":
                        return

                except json.JSONDecodeError:
                    yield {"error": "JSON解析失败", "raw": event}
                except Exception as e:
                    yield {"error": str(e), "raw": event}

        # 处理残余数据
        if buffer.strip():
            yield {"warning": "不完整数据片段", "remaining": buffer}

    return event_generator()


def _process_stream_event(event_data, status_context):
    """处理单个流式事件"""
    event_type = event_data.get("event")
    base_info = {
        'event': event_type,
        'task_id': event_data.get("task_id"),
        'workflow_run_id': event_data.get("workflow_run_id"),
        'timestamp': event_data.get("created_at")
    }

    handlers = {
        "workflow_started": lambda: {
            **base_info,
            "type": "metadata",
            "workflow_id": event_data["data"]["workflow_id"],
            "sequence": event_data["data"]["sequence_number"]
        },
        "node_started": lambda: {
            **base_info,
            "type": "node_start",
            "node_id": event_data["data"]["node_id"],
            "node_type": event_data["data"]["node_type"],
            "node_title": event_data["data"]["title"]
        },
        "node_finished": lambda: {
            **base_info,
            "type": "node_end",
            "node_id": event_data["data"]["node_id"],
            "status": event_data["data"]["status"],
            "elapsed": event_data["data"].get("elapsed_time"),
            "tokens": event_data["data"].get("execution_metadata", {}).get("total_tokens")
        },
        "message": lambda: {
            **base_info,
            "type": "content",
            "text": event_data.get("answer", "")
        },
        "workflow_finished": lambda: {
            **base_info,
            "type": "final_result",
            "status": event_data["data"]["status"],
            "total_time": event_data["data"]["elapsed_time"],
            "total_tokens": event_data["data"]["total_tokens"],
            "outputs": status_context['outputs'].update(
                event_data["data"].get("outputs", {})
            ) or status_context['outputs']
        },
        "tts_message": lambda: {
            **base_info,
            "type": "audio",
            "audio_data": event_data["audio"],
            "message_id": event_data["message_id"]
        }
    }

    # 执行事件处理并更新上下文
    if event_type == "workflow_started":
        status_context.update({
            'workflow_id': event_data["data"]["workflow_id"],
            'start_time': event_data["data"]["created_at"]
        })
    elif event_type == "node_started":
        status_context['current_node'] = event_data["data"]['node_id']
    elif event_type == "workflow_finished":
        status_context['outputs'] = event_data["data"].get("outputs", {})

    return handlers.get(event_type, lambda: {
        **base_info,
        "type": "unknown",
        "raw_data": event_data
    })()
