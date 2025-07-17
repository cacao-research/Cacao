/**
 * Range Sliders Component
 * Provides a dual-slider component for selecting a range of values
 */

function createRangeSliders(component) {
    const container = document.createElement("div");
    container.className = "range-sliders-container";
    
    // Create sliders container
    const slidersContainer = document.createElement("div");
    slidersContainer.className = "sliders-wrapper";
    
    // Create lower slider
    const lowerSlider = document.createElement("input");
    lowerSlider.type = "range";
    lowerSlider.className = "range-slider lower";
    lowerSlider.min = component.props.min;
    lowerSlider.max = component.props.max;
    lowerSlider.step = component.props.step;
    lowerSlider.value = component.props.lowerValue;

    // Create upper slider
    const upperSlider = document.createElement("input");
    upperSlider.type = "range";
    upperSlider.className = "range-slider upper";
    upperSlider.min = component.props.min;
    upperSlider.max = component.props.max;
    upperSlider.step = component.props.step;
    upperSlider.value = component.props.upperValue;

    // Add value displays
    const lowerDisplay = document.createElement("div");
    lowerDisplay.className = "range-value lower";
    lowerDisplay.textContent = `$${component.props.lowerValue}`;

    const upperDisplay = document.createElement("div");
    upperDisplay.className = "range-value upper";
    upperDisplay.textContent = `$${component.props.upperValue}`;

    const rangeDisplay = document.createElement("div");
    rangeDisplay.className = "range-display";
    rangeDisplay.appendChild(lowerDisplay);
    rangeDisplay.appendChild(document.createTextNode(" - "));
    rangeDisplay.appendChild(upperDisplay);

    let updateTimeout;
    const updateValues = async () => {
        const lower = parseFloat(lowerSlider.value);
        const upper = parseFloat(upperSlider.value);
        
        // Ensure lower value doesn't exceed upper value and vice versa
        if (lower > upper) {
            if (lowerSlider === document.activeElement) {
                upperSlider.value = lower;
            } else {
                lowerSlider.value = upper;
            }
        }
         
        // Update displays immediately
        lowerDisplay.textContent = `$${lowerSlider.value}`;
        upperDisplay.textContent = `$${upperSlider.value}`;

        if (component.props.onChange) {
            clearTimeout(updateTimeout);
            updateTimeout = setTimeout(async () => {
                try {
                    document.querySelector('.refresh-overlay').classList.add('active');
                    
                    const action = component.props.onChange.action;
                    const params = {
                        ...component.props.onChange.params,
                        lower_value: lowerSlider.value,
                        upper_value: upperSlider.value
                    };
                    
                    const queryParams = Object.entries(params)
                        .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
                        .join('&');
                        
                    const response = await fetch(`/api/event?event=${action}&${queryParams}&t=${Date.now()}`, {
                        method: 'GET',
                        headers: {
                            'Cache-Control': 'no-cache, no-store, must-revalidate'
                        }
                    });
                    
                    if (!response.ok) {
                        throw new Error(`Server returned ${response.status}`);
                    }
                    
                    const data = await response.json();
                    if (data.lower_value !== undefined) {
                        lowerSlider.value = data.lower_value;
                    }
                    if (data.upper_value !== undefined) {
                        upperSlider.value = data.upper_value;
                    }
                    window.CacaoWS.requestServerRefresh();
                } catch (err) {
                    console.error('[CacaoCore] Error updating range:', err);
                    document.querySelector('.refresh-overlay').classList.remove('active');
                }
            }, 100); // Debounce updates
        }
    };

    // Assemble the component
    slidersContainer.appendChild(lowerSlider);
    slidersContainer.appendChild(upperSlider);
    container.appendChild(slidersContainer);
    container.appendChild(rangeDisplay);

    // Add event listeners
    lowerSlider.addEventListener('input', updateValues);
    upperSlider.addEventListener('input', updateValues);
    
    return container;
}

// Export for component system
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { createRangeSliders };
}

// Register with global component system
if (typeof window !== 'undefined' && window.CacaoComponents) {
    window.CacaoComponents.register('range-sliders', createRangeSliders);
}