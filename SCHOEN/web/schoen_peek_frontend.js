import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
    name: "SCHOEN.Peek.UI", // GEÄNDERT
    async nodeCreated(node) {
        if (node.comfyClass !== "SchoenPeek") return;

        let isWorkflowLoopActive = false;
        let workflowTimeoutId = null;

        node.onDrawBackground = null;

        const previewImage = document.createElement("img");
        previewImage.style.width = "100%";
        previewImage.style.objectFit = "contain";
        previewImage.style.display = "none";

        const captureAndRefreshPreview = async () => {
            const res = await fetch(`/custom/SchoenPeek/capture_image`, { method: "POST" });
            const data = await res.json();
            if (data.preview) {
                previewImage.src = "data:image/jpeg;base64," + data.preview;
                previewImage.style.display = "block";
            }
        };

        node.addWidget("button", "⌖ Set Region", null, async () => {
            await fetch(`/custom/SchoenPeek/select_region`, { method: "POST" });
        });

        node.addWidget("button", "● Capture Now", null, captureAndRefreshPreview);

        const stopWorkflowLoop = () => {
            if (!isWorkflowLoopActive) return;
            isWorkflowLoopActive = false;
            if (workflowTimeoutId) {
                clearTimeout(workflowTimeoutId);
                workflowTimeoutId = null;
            }
            console.log("[SCHOEN Peek] Workflow Loop stopped."); // GEÄNDERT
        };

        node.addWidget("button", "▶ Start Live", null, async () => {
            const modeWidget = node.widgets.find(w => w.name === "mode");
            if (modeWidget.value !== "Live") {
                alert("Please switch to 'Live' mode to start the workflow loop.");
                return;
            }
            if (isWorkflowLoopActive) return;
            isWorkflowLoopActive = true;
            console.log("[SCHOEN Peek] Workflow Loop started."); // GEÄNDERT

            await captureAndRefreshPreview();
            app.queuePrompt();
        });

        node.addWidget("button", "■ Stop Live", null, stopWorkflowLoop);

        const modeWidget = node.widgets.find(w => w.name === "mode");
        if (modeWidget) {
            const originalCallback = modeWidget.callback;
            modeWidget.callback = (value) => {
                if (value === "Manual") {
                    stopWorkflowLoop();
                }
                return originalCallback?.(value);
            };
        }

        const onQueueEnd = (event) => {
            if (isWorkflowLoopActive && event.detail?.exec_info?.queue_remaining === 0) {
                const intervalWidget = node.widgets.find(w => w.name === "refresh_interval");
                const intervalSeconds = intervalWidget ? intervalWidget.value : 1.0;

                workflowTimeoutId = setTimeout(async () => {
                    if (!isWorkflowLoopActive) return;
                    await captureAndRefreshPreview();
                    app.queuePrompt();
                }, intervalSeconds * 1000);
            }
        };

        api.addEventListener("status", onQueueEnd);

        const onRemoved = node.onRemoved;
        node.onRemoved = () => {
            stopWorkflowLoop();
            api.removeEventListener("status", onQueueEnd);
            return onRemoved?.();
        };

        const container = document.createElement("div");
        container.style.width = "100%";
        container.style.marginTop = "10px";
        container.appendChild(previewImage);
        node.addDOMWidget("preview", "preview", container);
        previewImage.onload = () => {
            node.setDirtyCanvas(true);
        };
    },
});