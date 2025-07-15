(component) => {
    console.log("[CacaoCore] Rendering plot component:", component);
    
    // Create main element
    const el = document.createElement("div");
    el.className = "plot";
    
    // Add plot-specific styling
    if (component.props.width) {
        el.style.width = component.props.width;
    }
    if (component.props.height) {
        el.style.height = component.props.height;
    }
    
    // Create placeholder content for plot
    const plotContent = document.createElement("div");
    plotContent.className = "plot-content";
    
    // Add title if provided
    if (component.props.title) {
        const title = document.createElement("h3");
        title.className = "plot-title";
        title.textContent = component.props.title;
        el.appendChild(title);
    }
    
    // Add plot data visualization placeholder
    const plotArea = document.createElement("div");
    plotArea.className = "plot-area";
    plotArea.style.border = "1px solid #ddd";
    plotArea.style.borderRadius = "4px";
    plotArea.style.padding = "20px";
    plotArea.style.textAlign = "center";
    plotArea.style.backgroundColor = "#f9f9f9";
    plotArea.style.minHeight = "200px";
    plotArea.style.display = "flex";
    plotArea.style.alignItems = "center";
    plotArea.style.justifyContent = "center";
    
    // Add plot type indicator
    const plotType = component.props.type || "chart";
    plotArea.innerHTML = `
        <div style="color: #666;">
            <div style="font-size: 48px; margin-bottom: 10px;">📊</div>
            <div>Plot (${plotType})</div>
            ${component.props.data ? `<div style="font-size: 12px; margin-top: 5px;">Data points: ${Array.isArray(component.props.data) ? component.props.data.length : 'N/A'}</div>` : ''}
        </div>
    `;
    
    el.appendChild(plotArea);
    
    return el;
}