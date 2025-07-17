// Slider Component Renderer
(component) => {
    const slider = document.createElement("input");
    slider.type = "range";
    slider.className = component.props.className || "range-slider";
    slider.min = component.props.min;
    slider.max = component.props.max;
    slider.step = component.props.step;
    slider.value = component.props.value;

    let updateTimeout;
    const updateValue = async () => {
        if (component.props.onChange) {
            clearTimeout(updateTimeout);
            updateTimeout = setTimeout(async () => {
                try {
                    // Optionally show overlay
                    // document.querySelector('.refresh-overlay').classList.add('active');
                    const action = component.props.onChange.action;
                    const params = {
                        ...component.props.onChange.params,
                        value: slider.value
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
                    if (data.value !== undefined) {
                        slider.value = data.value;
                    }
                    window.CacaoWS.requestServerRefresh();
                } catch (err) {
                    console.error('[CacaoCore] Error updating slider:', err);
                    // document.querySelector('.refresh-overlay').classList.remove('active');
                }
            }, 200);
        }
    };
    slider.addEventListener('input', updateValue);
    return slider;
}