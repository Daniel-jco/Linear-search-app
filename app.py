import gradio as gr

MAX_SIZE = 100


# HTML Rendering for Array Visualization
def render_array_html(arr, highlight_index):
    """
    Generate an HTML block representing the array and highlight one element.

    Args:
        arr (list of int/float):
        highlight_index (int):

    Returns:
            An HTML string. Each element is displayed as a styled <div>.
    """
    html_elements = []

    for i, val in enumerate(arr):

        color = "#4CAF50" if i == highlight_index else "#e0e0e0"

        # Build the HTML chunk for current  array element.
        html_elements.append(f"""
            <div style="
                display:inline-block;
                margin:5px;
                padding:10px 15px;
                border-radius:8px;
                background-color:{color};
                font-weight: bold;
                min-width: 30px;
                text-align:center;
                font-family: monospace;
            ">{val}</div>
        """)

    # Wrap everything in a parent <div> container.
    return "<div>" + "".join(html_elements) + "</div>"

def parse_number(s):
    """
    Convert a given string to an integer or float if possible. Otherwise raises an error using gr.info()
    """
    s = s.strip()
    if not s:
        raise ValueError("Empty string is not a valid number")

    # Try integer conversion first; catch and pass if fail.
    try:
        return int(s)
    except ValueError:
        pass

    # Try float conversion.
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"Invalid number: '{s}'")


def compute_step(arr, target, index):
    """
    Compute the HTML visualization, status message, button state, and
    detection result for a given step of linear search. Called every time the next step or start search button is clicked

    Returns:
        tuple:
            (html : str,
             message : str,
             next_btn_state : gr.update,
             found : bool)
    """
    # Test for target match.
    found = arr[index] == target

    # Render the array with the active element highlighted.
    html = render_array_html(arr, index)

    if found:
        message = f"Found target at index {index}!"
    else:
        message = f"Target not found at index {index}."

    #disable the next button if the target was found this step
    next_btn_state = gr.update(interactive=not found)

    return html, message, next_btn_state, found


def error_state(msg):
    """
    Helper function used to display an error message using gr.info()

    Args:
        msg (str):
            Message to display as an error alert.

    Returns:
        html : str,
        message : str,
        state : dict,
        next_btn_state : gr.update()
        complete_btn_state: gr.update()
    """
    gr.Info(msg)

    # Reset state so the user can enter a new input
    empty_state = {
        "array": [],     
        "target": None,  
        "index": 0       
    }

    # Disable the next step button
    disabled_btn = gr.update(interactive=False)

    return "", "", empty_state, disabled_btn, disabled_btn


def start_search(array_input, target):
    """
    Parses the input, renders the html array, and calls compute_step()
   
    Returns:
        (html : str,
        message : str,
        state : dict,
        next_btn_state : gr.update()
        complete_btn_state : gr.update()
    """
    #parses each number in the input seprately
    try:
        arr = [
            parse_number(x)
            for x in array_input.split(",")
            if x.strip() 
        ]
    except ValueError as e:
        # If parsing fails, return error UI state.
        return error_state(f"ERROR! {e}")

    if len(arr) == 0 or len(arr) > MAX_SIZE:
        return error_state(
            f"ERROR: Array length must be between 1 and {MAX_SIZE}"
        )

    #initialize state
    state = {
        "array": arr,
        "target": target,
        "index": 0  # Start by examining index 0
    }

    #check index 0
    html, message, next_btn_state, found = compute_step(arr, target, 0)

    # If target not found at index 0, increment index for next step
    if not found:
        state["index"] = 1
    else:
        state["index"] = 0

    complete_btn_state = gr.update(interactive=not found)
    return html, message, state, next_btn_state, complete_btn_state


def next_step(state):
    """
    This function is called repeatedly via the next step button.
    Uses complete step to highlight current element and determine if it is the target

    Returns:
        html : str,
        message : str,
        state : dict,
        next_btn_state : gr.update()
        complete_btn_state: gr.update()
    """
    arr = state["array"]
    target = state["target"]
    index = state["index"]

    # If array is empty or we've examined all items then target is not in array
    if not arr or index >= len(arr):
        final_html = render_array_html([], -1)
        final_message = "Target not found in array."
        return final_html, final_message, state, gr.update(interactive=False)

    html, message, next_btn_state, found = compute_step(arr, target, index)

    # If still searching increment the index
    if not found:
        state["index"] = index + 1

    return html, message, state, next_btn_state, gr.update(interactive = False)

import time

def complete_search(state):
    """
    Automatically completes the search with a 0.5-second delay between steps.
    Uses yield so that the output can be streamed (i.e. so that the UI can be updated each step)
    """
    arr = state["array"]
    target = state["target"]
    index = state["index"]

    # Loop through remaining steps
    while index < len(arr):
        html, msg, next_btn_state, found = compute_step(arr, target, index)

        # Yield the UI update for this step
        yield html, msg, state, gr.update(interactive = False), gr.update(interactive = False)

        # If found, stop early
        if found:
            return

        index += 1
        state["index"] = index

        time.sleep(0.5)  # delay between steps

    # If we exit loop without finding the target
    html = render_array_html(arr, -1)
    msg = "Target not found in array."
    yield html, msg, state, gr.update(interactive=False), gr.update(interactive = False) #We want the next button and the complete button to not be interactable. 


# GRADIO UI SETUP
with gr.Blocks() as demo:

    gr.Markdown("# Linear Search Visualizer")
    gr.Markdown("### By Daniel Cohen")

    # Inputs
    array_input = gr.Textbox(
        label="Array (comma separated)",
        placeholder="Example: 5, 12, 3, 9"
    )

    target_input = gr.Number(
        label="Target",
    )

    # Buttons
    start_btn = gr.Button("Start Search")
    next_btn = gr.Button("Next Step", interactive=False)
    complete_btn = gr.Button("Complete Search", interactive=False)


    # Outputs
    array_visual = gr.HTML()    # Displays the array
    message = gr.Markdown()     # Displays search status text
    state = gr.State()          # State containing the array, target, and current index

    gr.Markdown("-------------------------------------------------------------------------------------")
    gr.Markdown("# How it works")
    gr.Markdown("Linear search is the simplest sorting algorithm there is. We are given an array and a target. Starting at index zero, we iterate through the array checking each index to see if the target is at that position in the list. If not, we keep going until the end of the list. When the target is found, we return the index of the list where we found it. If we reach the end of the list without finding it, we return that the target was not in the array. This can be done by simply returning -1.")
    start_btn.click(
        start_search,
        inputs=[array_input, target_input],
        outputs=[array_visual, message, state, next_btn, complete_btn]
    )

    next_btn.click(
        next_step,
        inputs=state,
        outputs=[array_visual, message, state, next_btn, complete_btn]
    )

    complete_btn.click(
    complete_search,
    inputs=state,
    outputs=[array_visual, message, state, next_btn, complete_btn],
    )


demo.launch()