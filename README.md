---
title: Linear Search App
emoji: "🔍"
colorFrom: green
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
---

# Linear Search Visualizer

## Why I chose Linear Search
Linear search was the first sorting algorithm I learned, and like most people, I was using it before I really knew what a searching algorithm was. Needing to find a target element in an unsorted array is an extremeley common problem, and it has an extremely intuitive solution: loop through the array and check each element. Many people figure out this solution on their own before the idea of "searching algorithm" is even taught, simply because it comes up so often. It is not the most efficient searching algorithm, but it may very well be the most versatile. I have had no experience working with GUI before, so I figured that choosing a simple, intuitive searching algorithm would allow me to focus on learning the basics of gradio. 

## Demo video/screenshots of test
![alt text](<Screenshot 1.png>)
![alt text](<Screenshot 2.png>)
<video controls src="Demo Video.mp4" title="Title"></video>

## Problem Breakdown & Computational Thinking 
### Decomposition
Smaller steps included:
For gradio:
- Getting the input array and target value from the user
- Checking that the input was valid (no empty lists, must be within input size, can't enter letters instead of numbers)
- Parsing the input from a string to a list of ints and floats 
- Rendering the input array as squares using HTML and highlighting the current square green (when the start button is pressed)
- Highlight the new current element when index is incremented
- Display a message to the user telling them which index we are currently checking and if we found the target
- If we find the target, deactivate the next step button
- If we reach the end of the list without finding the target, tell the user that the target is not in the array and deactivate the next step button

For linear search in general:
- Get the input array and target value from the user
- Iterate through the array, checking if each element is the target
- If it is, return the index of the target. If not, continue stepping through array
- If we reach the end without finding the target, return that it was not in the array

### Pattern Recognition
- Linear search repeatedly compares the target value to the value of the list at the current index. This pattern is repeated every iteration until the end of the list is reached
- The index goes up by one each time, and stops when a maximum value (the length of the list) is reached
- This pattern is indicative of a for loop, however a while loop can work as well if a counter is manually incremented and a base case is set.

### Abstraction
- The user should see the list itself and should see the current index of the list being indicated somehow
- The user does not need to see the process of their input being validated, but they should receive an error message if their input is invalid
- The user should also be able to see a status on the current element, i.e. if the current element is the target or if we need to keep searching. They should also see that the target element is not in the array if this is found to be the case

### Algorithm Design
- The user should have an input box where they can enter their target value and their array. They should be able to enter the array in some intuitive way, i.e. they shouldn't have to format it like [1, 2, 3, 4]. It should be flexible
- Their input would be initially a string, so we would need to parse it into an actual array of numbers (floats or ints)
- We would then be able to work with the numbers, so we can go through the algorithm step by step to check if we have found the target value
- The process should be visually shown to the user while it happens. Internally the array will be a list of numbers but it should show something visual to the user. I am not yet familiar with the gradio GUI so I am not exactly sure how it will be displayed, but it is important that they can see what the current element is.
- The user should also see an output box where we can display if they target has been found at the current index, if the target has not been found at the current index, or if the target is not in the array. 
![alt text](Linear_Search_Flowchart.png)

## Steps to Run
Simply enter a comma seperated array into the input box and a target value in the target box. You will then be able to click start search. Then just click the next step button to step through the algorithm. 

## Hugging Face Link


## Author & Acknowledgment
This app was created by Daniel Cohen. ChatGPT was used with usage level 4. It's main uses was writing draft code for the HTML components as well as suggesting refactors to improve modularity by creating helper functions compute_step() and error_state(). It was also used throughout the project for debugging and suggesting various gradio features that I could use for the project. 