(component) => {
    console.log("[CacaoCore] Rendering image component:", component);
    
    // Create main wrapper element
    const wrapper = document.createElement("div");
    wrapper.className = "image-wrapper";
    wrapper.style.display = "inline-block";
    wrapper.style.position = "relative";
    
    // Create image element
    const img = document.createElement("img");
    img.className = "image";
    
    // Set image source
    if (component.props.src) {
        img.src = component.props.src;
    } else {
        // Default placeholder image
        img.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' fill='%23f0f0f0'/%3E%3Ctext x='100' y='100' text-anchor='middle' dominant-baseline='middle' font-family='Arial' font-size='14' fill='%23999'%3ENo Image%3C/text%3E%3C/svg%3E";
    }
    
    // Set alt text
    img.alt = component.props.alt || "Image";
    
    // Set dimensions
    if (component.props.width) {
        img.style.width = typeof component.props.width === 'number' ? `${component.props.width}px` : component.props.width;
    }
    if (component.props.height) {
        img.style.height = typeof component.props.height === 'number' ? `${component.props.height}px` : component.props.height;
    }
    
    // Set object fit
    if (component.props.fit) {
        img.style.objectFit = component.props.fit;
    }
    
    // Add border radius if specified
    if (component.props.radius) {
        img.style.borderRadius = typeof component.props.radius === 'number' ? `${component.props.radius}px` : component.props.radius;
    }
    
    // Add border if specified
    if (component.props.bordered) {
        img.style.border = "1px solid #ddd";
    }
    
    // Handle preview/zoom functionality
    if (component.props.preview) {
        img.style.cursor = "pointer";
        img.addEventListener("click", () => {
            // Create modal overlay
            const overlay = document.createElement("div");
            overlay.style.position = "fixed";
            overlay.style.top = "0";
            overlay.style.left = "0";
            overlay.style.width = "100%";
            overlay.style.height = "100%";
            overlay.style.backgroundColor = "rgba(0,0,0,0.8)";
            overlay.style.display = "flex";
            overlay.style.alignItems = "center";
            overlay.style.justifyContent = "center";
            overlay.style.zIndex = "9999";
            overlay.style.cursor = "pointer";
            
            // Create preview image
            const previewImg = document.createElement("img");
            previewImg.src = img.src;
            previewImg.alt = img.alt;
            previewImg.style.maxWidth = "90%";
            previewImg.style.maxHeight = "90%";
            previewImg.style.objectFit = "contain";
            
            overlay.appendChild(previewImg);
            
            // Close modal when clicking overlay
            overlay.addEventListener("click", () => {
                document.body.removeChild(overlay);
            });
            
            // Close modal with Escape key
            const handleEscape = (e) => {
                if (e.key === "Escape") {
                    document.body.removeChild(overlay);
                    document.removeEventListener("keydown", handleEscape);
                }
            };
            document.addEventListener("keydown", handleEscape);
            
            document.body.appendChild(overlay);
        });
    }
    
    // Add loading state
    const loadingIndicator = document.createElement("div");
    loadingIndicator.className = "image-loading";
    loadingIndicator.style.position = "absolute";
    loadingIndicator.style.top = "50%";
    loadingIndicator.style.left = "50%";
    loadingIndicator.style.transform = "translate(-50%, -50%)";
    loadingIndicator.style.color = "#999";
    loadingIndicator.style.fontSize = "12px";
    loadingIndicator.textContent = "Loading...";
    
    // Add error state
    const errorIndicator = document.createElement("div");
    errorIndicator.className = "image-error";
    errorIndicator.style.position = "absolute";
    errorIndicator.style.top = "50%";
    errorIndicator.style.left = "50%";
    errorIndicator.style.transform = "translate(-50%, -50%)";
    errorIndicator.style.color = "#ff4757";
    errorIndicator.style.fontSize = "12px";
    errorIndicator.style.display = "none";
    errorIndicator.textContent = "Failed to load";
    
    // Handle loading events
    img.addEventListener("load", () => {
        loadingIndicator.style.display = "none";
        errorIndicator.style.display = "none";
    });
    
    img.addEventListener("error", () => {
        loadingIndicator.style.display = "none";
        errorIndicator.style.display = "block";
        
        // Set fallback image if provided
        if (component.props.fallback) {
            img.src = component.props.fallback;
        }
    });
    
    // Add lazy loading if specified
    if (component.props.lazy) {
        img.loading = "lazy";
    }
    
    // Add caption if provided
    if (component.props.caption) {
        const caption = document.createElement("div");
        caption.className = "image-caption";
        caption.style.textAlign = "center";
        caption.style.marginTop = "8px";
        caption.style.fontSize = "14px";
        caption.style.color = "#666";
        caption.textContent = component.props.caption;
        
        wrapper.appendChild(img);
        wrapper.appendChild(loadingIndicator);
        wrapper.appendChild(errorIndicator);
        wrapper.appendChild(caption);
    } else {
        wrapper.appendChild(img);
        wrapper.appendChild(loadingIndicator);
        wrapper.appendChild(errorIndicator);
    }
    
    return wrapper;
}