import gradio as gr

MAX_BUTTONS = 50  # maximum number of buttons we'll show

def start_search(array_input, target):

    # Convert input string to list of integers
    try:
        arr = [int(x.strip()) for x in array_input.split(",") if x.strip() != ""]
    except Exception as e:
        message = f"ERROR! Invalid input"
        state = {"array": [], "target": target, "index": 0}
        next_btn_update = gr.update(interactive = False)
        gr.Info(message) # Added
        # return (*btn_updates, message, state, next_btn_update)
    
    # Error handling
    if len(arr) > MAX_BUTTONS or not arr:
        message = "ERROR: Input size greater than 50 (or less than 1) is not supported."
        state = {"array": [], "target": target, "index": 0}
        next_btn_update = gr.update(interactive = False)
        gr.Info(message) # Added
    
    state = {
        "array": arr,
        "target": target,
        "index": 0  # start at first element
    }

    # Update pre-created buttons
    btn_updates = []
    for i in range(MAX_BUTTONS):
        if i < len(arr):
            variant = "primary" if i == 0 else "secondary"
            btn_updates.append(gr.update(
                value=str(arr[i]),
                interactive=False,
                variant=variant,
                visible=True
            ))
        else:
            btn_updates.append(gr.update(
                value="",
                visible=False
            ))

    # Initial message
    state["index"] += 1
    message = "Found target at index 0!" if arr and arr[0] == target else "Target not found at index 0"

    next_btn_update = gr.update(interactive=True)
    return (*btn_updates, message, state, next_btn_update)

def next_step(state):
    arr = state["array"]
    target = state["target"]
    index = state["index"]

    # Safety: if we've already reached end
    if index >= len(arr):
        next_btn_update = gr.update(interactive=False)
        return (*[gr.update(visible=False) for i in range(MAX_BUTTONS)],
                "Target not in array",
                state, next_btn_update)

    # Update buttons to move the highlight
    btn_updates = []
    for i in range(MAX_BUTTONS):
        if i < len(arr):
            variant = "primary" if i == index else "secondary"
            btn_updates.append(gr.update(
                value=str(arr[i]),
                interactive=False,
                variant=variant,
                visible=True
            ))
        else:
            btn_updates.append(gr.update(
                value="",
                visible=False
            ))

    # Update message
    if arr[index] == target:
        message = f"Found target at index {index}"
        next_btn_update = gr.update(interactive=False)
    else:
        message = f"Target not found at index {index} "
        next_btn_update = gr.update(interactive = True)

    # Increment index safely
    if index + 1 < len(arr):
        state["index"] = index + 1
    else:
        state["index"] = len(arr)  # mark that we've finished

    return (*btn_updates, message, state, next_btn_update)

# ---------------- Gradio Interface ----------------
demo = gr.Blocks()

with demo:
    H1 = gr.Markdown("# LINEAR SEARCH")
    H2 = gr.Markdown("### By Daniel Cohen")
    H3 = gr.Markdown("### Note: The start search button must be clicked twice the first time!")
    array_input = gr.Textbox(label="Array (comma-separated, n<50)")
    target_input = gr.Number(label="Target")
    
    # Pre-create buttons (hidden at start)
    with gr.Row() as button_row:
        btns = [gr.Button("", interactive=False, visible=False, scale=1) for _ in range(MAX_BUTTONS)]

    start_btn = gr.Button("Start Search")
    next_btn = gr.Button("Next Step")
    status = gr.Markdown("### STATUS:")
    message_box = gr.Markdown()
    state = gr.State()

    start_btn.click(
        start_search,
        inputs=[array_input, target_input],
        outputs=[*btns, message_box, state, next_btn]
    )

    next_btn.click(
        next_step,
        inputs=state,
        outputs=[*btns, message_box, state, next_btn]
    )

demo.launch()
