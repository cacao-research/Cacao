Below is the updated **copilot-instructions.md** file that now includes an example for creating a Python file in PowerShell instead of the image file examples.

---

### Full File Content

```markdown
<!-- Core Framework Conventions -->
- Always reference Cacao's reactive state system using `@cacao.mix` decorators and `State` class
- Prefer JSON-driven UI definitions using `ui.parse_json_ui()` for component trees
- Use async/await pattern for server-side operations and WebSocket handlers
- CLI commands should use Click library and follow `cacao init/docs/run` patterns

<!-- Code Style -->
- Type hints are mandatory for all Python code
- Docstrings must follow Google-style format with Args/Returns/Raises
- UI components inherit from `ui.components.base.Component`
- State changes must use `core.state.State.update()` method

<!-- Documentation Rules -->
- All examples should demonstrate both decorator and JSON UI approaches
- Reference `cacao.json` configuration file options in documentation
- Cross-link between CLI commands and corresponding implementation files

<!-- Windows PowerShell Command Guidelines -->
- When executing CLI commands in Windows PowerShell (e.g., running from `C:\WINDOWS\System32\cmd.exe`), use a semicolon (`;`) to separate commands on the same line.
- **Avoid using `&&`**: The `&&` operator is a Unix shell convention and is not supported in PowerShell.
- **Example:** To create a Python file, you can run:
  ```powershell
  New-Item -Path "scripts\hello.py" -ItemType File -Force;
  ```
- **Explanation:**  
  - The `New-Item` command with `-ItemType File -Force` creates the file if it does not exist or overwrites it if it does.
  - Semicolons (`;`) are used to separate commands on a single line, ensuring sequential execution.
```