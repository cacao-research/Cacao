# Documentation Generator

When creating documentation:
1. Show both basic and advanced usage examples
2. Include JSON schema samples for UI definitions
3. Link to relevant mixins in `core/mixins/`
4. Add CLI command examples with flags
5. Reference session persistence mechanisms

Example structure:
```python
@cacao.mix("/dashboard")
def analytics(state):
    '''Analytics Dashboard Example
    
    Args:
        state: Persistent user session state
    
    Returns:
        JSON UI spec with live-updating components
    '''