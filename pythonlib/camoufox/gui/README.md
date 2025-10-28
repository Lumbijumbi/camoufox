# Camoufox GUI - Playwright Automation Tool

A graphical user interface for recording and automating browser interactions with Camoufox and Playwright.

## Features

- 🎯 **Target URL Input**: Easily specify the starting URL for your automation
- ⚙️ **Flexible Options**: Configure browser settings including:
  - Headless mode toggle
  - Custom viewport dimensions
  - Language settings
  - Output format selection (Python, Python-async, JavaScript, Java, C#)
- 🔴 **Record Flow**: Capture browser interactions in real-time using Playwright's codegen
- 💾 **Save Scripts**: Export generated automation scripts to files
- 🗑️ **Clear Output**: Reset the code area when needed
- 📊 **Status Tracking**: Monitor recording state with visual feedback

## Usage

### Launching the GUI

You can launch the Camoufox GUI in several ways:

#### From Command Line

```bash
camoufox gui
```

or

```bash
python -m camoufox gui
```

#### From Python Code

```python
from camoufox.gui import launch_gui

launch_gui()
```

## How to Use

1. **Enter Target URL**: Type or paste the URL where you want to start recording (e.g., `https://example.com`)

2. **Configure Options** (optional):
   - Toggle **Headless Mode** if you want the browser to run without a visible window
   - Set **Viewport** dimensions (width x height) for the browser window
   - Specify **Language** preference (e.g., `en-US`, `fr-FR`)
   - Choose **Output Format** for the generated script

3. **Start Recording**:
   - Click the "🔴 Start Recording" button
   - A browser window will open (unless in headless mode)
   - Interact with the website normally (click, type, navigate, etc.)
   - All your actions will be recorded automatically

4. **Stop Recording**:
   - Click the "⏹️ Stop Recording" button when finished
   - The generated code will appear in the output area

5. **Save Script**:
   - Review the generated code
   - Click "💾 Save Script" to export to a file
   - Choose a location and filename

6. **Run Your Script**:
   - The saved script can be executed directly
   - For Python scripts: `python your_script.py`
   - For other languages: compile/run according to that language's requirements

## Example Workflow

1. Launch GUI: `camoufox gui`
2. Enter URL: `https://github.com`
3. Set viewport: `1920 x 1080`
4. Select format: `python-async`
5. Click "Start Recording"
6. Perform actions in the browser:
   - Navigate to login page
   - Enter credentials
   - Click login button
7. Click "Stop Recording"
8. Review generated code
9. Click "Save Script" → save as `github_login.py`
10. Run: `python github_login.py`

## Generated Code Examples

### Python (Sync)
```python
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://example.com")
    # Your recorded actions...
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
```

### Python (Async)
```python
import asyncio
from playwright.async_api import async_playwright

async def run(playwright):
    browser = await playwright.firefox.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://example.com")
    # Your recorded actions...
    await context.close()
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())
```

## Tips

- **Test your target URL first**: Make sure the website is accessible before recording
- **Plan your actions**: Think through the steps you want to automate before recording
- **Use meaningful names**: When saving scripts, use descriptive filenames
- **Review generated code**: Always review and test generated scripts before production use
- **Edit as needed**: The generated code is a starting point - customize it for your needs

## Troubleshooting

### GUI won't launch
- Make sure `tkinter` is installed: `sudo apt-get install python3-tk` (Linux)
- On macOS and Windows, tkinter is usually included with Python

### Recording doesn't start
- Ensure Playwright is installed: `pip install playwright`
- Install browser drivers: `playwright install firefox`

### Browser path not found
- Make sure Camoufox binaries are downloaded: `camoufox fetch`

### Code area is empty after recording
- Check that you actually performed actions in the browser
- Try a longer recording session
- Look for error messages in the console

## Requirements

- Python 3.8+
- tkinter (usually included with Python)
- Playwright
- Camoufox binaries

## See Also

- [Camoufox Python Interface](../README.md)
- [Playwright Documentation](https://playwright.dev/)
- [Camoufox Main Documentation](https://camoufox.com/)
