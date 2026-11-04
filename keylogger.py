import logging
import sys
from pynput import keyboard
# 1. Use the standard logging module to handle file I/O safely.
# This automatically appends to the file ('a' mode) instead of overwriting ('w').
logging.basicConfig(
    filename="input_diagnostics.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def on_press(key):
    try:
        # 2. Handle standard alphanumeric keys
        if hasattr(key, 'char') and key.char is not None:
            log_message = f"Character Input: {key.char}"
        else:
            # 3. Handle special keys (Ctrl, Alt, Shift, Enter, etc.) systematically
           log_message = f"Special Key: {key}"
            
        # Write to log immediately to prevent data loss if the process is terminated
        logging.info(log_message)
        
    except AttributeError as e:
        logging.error(f"Attribute error processing key: {e}")
    except Exception as e:
        # 4. Prevent the listener from crashing due to unexpected write/processing errors
        logging.error(f"Unexpected error during input processing: {e}")

    # Define exit condition
    if key == keyboard.Key.esc:
        logging.info("Diagnostic session terminated by user.")
        return False

if __name__ == "__main__":

    try:
        # 5. Wrap the listener execution in a try-except block to handle system interrupts
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except PermissionError:
        print("Error: Insufficient permissions to register global input hooks.", file=sys.stderr)
    except Exception as e:
        print(f"Initialization failed: {e}", file=sys.stderr)
