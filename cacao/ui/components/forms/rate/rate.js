// Rate Component Renderer
(component) => {
    const wrapper = document.createElement("div");
    wrapper.className = "rate-wrapper";
    const max = component.props.max || 5;
    let value = component.props.value || 0;
    let hoverValue = null;

    function renderStars() {
        wrapper.innerHTML = "";
        for (let i = 1; i <= max; i++) {
            const star = document.createElement("span");
            star.className = "rate-star";
            // Half-star logic
            let fill = false;
            if (hoverValue !== null) {
                fill = i <= Math.floor(hoverValue);
                if (i === Math.ceil(hoverValue) && hoverValue % 1 >= 0.5) {
                    star.classList.add("half");
                }
            } else {
                fill = i <= Math.floor(value);
                if (i === Math.ceil(value) && value % 1 >= 0.5) {
                    star.classList.add("half");
                }
            }
            if (fill) star.classList.add("filled");
            star.textContent = "★";
            // Mouse events for half-star
            star.addEventListener("mousemove", (e) => {
                const rect = star.getBoundingClientRect();
                const x = e.clientX - rect.left;
                hoverValue = x < rect.width / 2 ? i - 0.5 : i;
                renderStars();
            });
            star.addEventListener("mouseleave", () => {
                hoverValue = null;
                renderStars();
            });
            star.addEventListener("click", (e) => {
                const rect = star.getBoundingClientRect();
                const x = e.clientX - rect.left;
                value = x < rect.width / 2 ? i - 0.5 : i;
                // Optionally: send event to backend here
                // If you want to send to backend:
                if (component.props.onChange) {
                    const action = component.props.onChange.action;
                    const params = {
                        ...component.props.onChange.params,
                        value: value
                    };
                    const queryParams = Object.entries(params)
                        .map(([key, val]) => `${key}=${encodeURIComponent(val)}`)
                        .join('&');
                    fetch(`/api/event?event=${action}&${queryParams}&t=${Date.now()}`, {
                        method: 'GET',
                        headers: {
                            'Cache-Control': 'no-cache, no-store, must-revalidate'
                        }
                    }).then(r => r.json()).then(data => {
                        if (data.value !== undefined) value = data.value;
                        window.CacaoWS.requestServerRefresh();
                    });
                }
                renderStars();
            });
            wrapper.appendChild(star);
        }
    }
    renderStars();
    return wrapper;
}