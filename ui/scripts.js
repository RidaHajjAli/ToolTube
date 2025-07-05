// ui/scripts.js

/**
 * Simulates a typing effect for the given text in the output textarea.
 * @param {string} text - The text to display with a typing effect.
 */
function type_effect(text) {
    if (!text) { return; }
    const textarea = document.querySelector('#output-box textarea');
    if (!textarea) return;
    textarea.value = '';
    let i = 0;
    function typing() {
        if (i < text.length) {
            textarea.value += text.charAt(i);
            i++;
            textarea.scrollTop = textarea.scrollHeight;
            setTimeout(typing, Math.random() * 40 + 5);
        }
    }
    typing();
    return text;
}

/**
 * Handles UI state for submission (button loading state).
 */
function handle_submission() {
    const submitBtn = document.getElementById('submit-button');
    if (submitBtn) {
        submitBtn.classList.add('processing');
        submitBtn.innerText = 'PROCESSING...';
        submitBtn.disabled = true;
    }
    const resetBtn = document.getElementById('reset-button');
    if (resetBtn) {
        resetBtn.disabled = true;
    }
}

/**
 * Resets the UI state after processing is complete.
 * Re-enables the submit button.
 */
function handle_completion() {
    const submitBtn = document.getElementById('submit-button');
    if (submitBtn) {
        submitBtn.classList.remove('processing');
        submitBtn.innerText = 'PROCESS REQUEST';
        submitBtn.disabled = false;
    }
    const resetBtn = document.getElementById('reset-button');
    if (resetBtn) {
        resetBtn.disabled = false;
    }
}

/**
 * @returns {Array<string>} An array of empty strings to clear the Gradio components.
 */
function reset_all() {
    const statusArea = document.getElementById('status-area');
    if (statusArea) {
        statusArea.innerHTML = '';
    }
    const submitBtn = document.getElementById('submit-button');
    if (submitBtn) {
        submitBtn.classList.remove('processing');
        submitBtn.innerText = 'PROCESS REQUEST';
        submitBtn.disabled = false;
    }
    return ["", "", ""];
}