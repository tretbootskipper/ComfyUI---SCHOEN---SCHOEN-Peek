# ComfyUI---SCHOEN---SCHOEN-Peek

`SCHOEN Peek` is the first node I created for an industrial design tool-set. It´s a versatile input node for ComfyUI that allows you to capture any area of your screen in real-time and use it as an image input for your workflows. 
It is ideal for interactive image generation, live feedback loops, or directly integrating external content like videos, designs, or games into your AI workflows.

The Node:
<img width="1041" height="505" alt="03 - node" src="https://github.com/user-attachments/assets/4627f301-64e8-42d1-bc72-afb90264740f" />


## ✨ Features

-   **Select Any Area:** Use your mouse to define the exact screen region you want to capture.
-   **Manual Mode:** Capture images with a button press, giving you full control over when the workflow starts.
-   **Intelligent Live Workflow:** Start an automatic loop that captures a new screenshot and re-runs the entire workflow after each completion, based on a customizable interval.
-   **Integrated Preview:** A live preview panel directly on the node shows you the currently captured image at all times.
-   **Lossless Quality:** While the preview is optimized for a smooth UI, the image passed to the workflow is captured in its full, lossless original resolution.

Set a Frame:
<img width="2560" height="1440" alt="01 - set frame" src="https://github.com/user-attachments/assets/462e120e-6165-44a8-a44f-e82a210532fd" />

Start your Workflow manual or live:
<img width="2560" height="1440" alt="02 - in action" src="https://github.com/user-attachments/assets/9cb97866-e407-4631-a833-f52f37e9bada" />

## 📦 Installation

1.  Navigate to the `ComfyUI/custom_nodes/` directory in your ComfyUI installation.
2.  Create a new folder named `SCHOEN`.
3.  Place the project files (`__init__.py`, `SchoenPeek.py`, and the `web` folder) inside this new `SCHOEN` folder.

Your final folder structure should look like this:

ComfyUI/custom_nodes/SCHOEN/ init.py + SchoenPeek.py + web/ schoen_peek_frontend.js

4.  **Install Dependencies:** This node requires `opencv-python`. Open a command line/terminal in your ComfyUI directory and install it into your Python environment:
    ```bash
    # Windows
    .\python_embeded\python.exe -m pip install opencv-python

    # Linux/macOS (adjust the path to your virtual environment)
    path/to/your/venv/bin/pip install opencv-python
    ```
5.  **Restart ComfyUI:** Completely shut down the ComfyUI terminal window and start it again.

## 🚀 How to Use

After installation, you can find the node via **"Add Node" → "SCHOEN" → "SCHOEN Peek"**.

### Manual Mode (Default)

This is the best mode for controlled, single-shot generations.

1.  Ensure the `mode` is set to **"Manual"**.
2.  Click `⌖ Set Region`. An overlay will appear on your screen. Drag a rectangle with your mouse over the desired area.
3.  Confirm your selection by pressing the **Enter** key. (Cancel with **Esc**).
4.  Click `● Capture Now` to capture the image. The preview will update.
5.  Run your workflow as usual by clicking "Queue Prompt".

### Automatic Workflow Mode

Perfect for live demos, experiments, or processing video content.

1.  Set the `mode` to **"Live"**.
2.  Adjust the `refresh_interval` (in seconds). This is the wait time *after* a workflow has finished.
3.  Click `⌖ Set Region` to define your capture area.
4.  Click `▶ Start Live`.
    -   The node immediately captures an image and starts the first workflow run.
    -   Once the workflow is complete, the node waits for the specified interval time.
    -   After the interval, it captures a new image and starts the next workflow run.
5.  Click `■ Stop Live` or switch the `mode` back to "Manual" to end the automatic process.

## 🛠️ UI Elements Explained

-   **`mode`**: Toggles between the "Manual" and automatic "Live" modes.
-   **`refresh_interval`**: The wait time in seconds in "Live" mode after a workflow run has completed.
-   **`⌖ Set Region`**: Opens the screen selection tool to define the capture area.
-   **`● Capture Now`**: Captures an image in Manual mode and updates the preview.
-   **`▶ Start Live`**: Starts the automatic workflow loop (only works in "Live" mode).
-   **`■ Stop Live`**: Ends the automatic workflow loop.
-   **Preview Panel**: Displays a small, optimized preview of the last captured image.

<img width="1041" height="505" alt="03 - node" src="https://github.com/user-attachments/assets/c44fccc1-9ab9-486b-9166-ed84d0040c14" />

## ⚠️ Known Limitations & Considerations

-   **Platform Compatibility:** This node has been developed and tested primarily on **Windows**.
    -   On **macOS**, you may need to grant screen recording permissions to your terminal or ComfyUI application in "System Settings" → "Privacy & Security".
    -   On **Linux**, functionality may depend on your display server (X11 is generally better supported by the underlying libraries than Wayland).
    -   Community feedback and testing on non-Windows platforms are highly appreciated!

-   **Multi-Monitor Setups:** The region selection tool might span across all available monitors, creating one large virtual canvas. This is the default behavior of the underlying library (`cv2.selectROI`).

-   **Dependencies:** The node requires `opencv-python`, which is a considerable dependency. It is necessary for the robust and user-friendly region selection feature.

## 🔧 Troubleshooting

-   **Buttons/Preview are missing (Frontend not loading):**
    -   Perform a "Hard Reload" in your browser (**Ctrl+Shift+R** on Windows/Linux, **Cmd+Shift+R** on Mac).
    -   Double-check that your folder structure exactly matches the one in the installation guide. The parent folder **must** be named `SCHOEN` and contain the `web` subfolder.
-   **The "Set Region" button does nothing:**
    -   This can happen if the ComfyUI server is blocked or frozen. Ensure you are using the latest version of the code.
    -   Check the ComfyUI console (the black terminal window) for any error messages when you press the button.

## 📜 License

This project is licensed under the MIT License.

This license permits you to do almost anything you want with the software, including using and modifying it for commercial purposes, as long as you include the original copyright notice and the license text in your distribution.
