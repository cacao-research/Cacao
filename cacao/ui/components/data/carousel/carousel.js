(component) => {
    console.log("[CacaoCore] Rendering carousel component:", component);
    
    // Create main element
    const el = document.createElement("div");
    el.className = "carousel";
    el.style.position = "relative";
    el.style.overflow = "hidden";
    el.style.border = "1px solid #ddd";
    el.style.borderRadius = "4px";
    
    // Set dimensions
    const width = component.props.width || "100%";
    const height = component.props.height || "300px";
    el.style.width = width;
    el.style.height = height;
    
    // Create items container
    const itemsContainer = document.createElement("div");
    itemsContainer.className = "carousel-items";
    itemsContainer.style.display = "flex";
    itemsContainer.style.transition = "transform 0.3s ease";
    itemsContainer.style.height = "100%";
    
    // Track current item
    let currentIndex = 0;
    let items = [];
    
    // Add items
    if (Array.isArray(component.props.items)) {
        items = component.props.items;
        component.props.items.forEach((item, index) => {
            const itemEl = document.createElement("div");
            itemEl.className = "carousel-item";
            itemEl.style.minWidth = "100%";
            itemEl.style.height = "100%";
            itemEl.style.display = "flex";
            itemEl.style.alignItems = "center";
            itemEl.style.justifyContent = "center";
            itemEl.style.backgroundColor = "#f9f9f9";
            itemEl.style.border = "1px solid #eee";
            
            if (typeof item === 'string') {
                itemEl.textContent = item;
            } else if (item.content) {
                if (typeof item.content === 'string') {
                    itemEl.textContent = item.content;
                } else {
                    itemEl.appendChild(window.CacaoCore.renderComponent(item.content));
                }
            } else {
                itemEl.innerHTML = `
                    <div style="text-align: center; color: #666;">
                        <div style="font-size: 48px; margin-bottom: 10px;">🖼️</div>
                        <div>Carousel Item ${index + 1}</div>
                    </div>
                `;
            }
            
            itemsContainer.appendChild(itemEl);
        });
    } else {
        // Default placeholder item
        const itemEl = document.createElement("div");
        itemEl.className = "carousel-item";
        itemEl.style.minWidth = "100%";
        itemEl.style.height = "100%";
        itemEl.style.display = "flex";
        itemEl.style.alignItems = "center";
        itemEl.style.justifyContent = "center";
        itemEl.style.backgroundColor = "#f9f9f9";
        itemEl.innerHTML = `
            <div style="text-align: center; color: #666;">
                <div style="font-size: 48px; margin-bottom: 10px;">🖼️</div>
                <div>Carousel</div>
            </div>
        `;
        itemsContainer.appendChild(itemEl);
        items = [{}]; // Single placeholder item
    }
    
    // Function to update carousel position
    const updateCarousel = () => {
        const translateX = -currentIndex * 100;
        itemsContainer.style.transform = `translateX(${translateX}%)`;
        
        // Update indicators
        const indicators = el.querySelectorAll('.carousel-indicator');
        indicators.forEach((indicator, index) => {
            indicator.style.backgroundColor = index === currentIndex ? '#007bff' : '#ccc';
        });
    };
    
    // Create navigation controls if more than one item
    if (items.length > 1) {
        // Previous button
        const prevBtn = document.createElement("button");
        prevBtn.className = "carousel-nav carousel-prev";
        prevBtn.innerHTML = "‹";
        prevBtn.style.position = "absolute";
        prevBtn.style.left = "10px";
        prevBtn.style.top = "50%";
        prevBtn.style.transform = "translateY(-50%)";
        prevBtn.style.backgroundColor = "rgba(0,0,0,0.5)";
        prevBtn.style.color = "white";
        prevBtn.style.border = "none";
        prevBtn.style.borderRadius = "50%";
        prevBtn.style.width = "40px";
        prevBtn.style.height = "40px";
        prevBtn.style.cursor = "pointer";
        prevBtn.style.fontSize = "18px";
        prevBtn.style.zIndex = "10";
        
        prevBtn.addEventListener("click", () => {
            currentIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
            updateCarousel();
        });
        
        // Next button
        const nextBtn = document.createElement("button");
        nextBtn.className = "carousel-nav carousel-next";
        nextBtn.innerHTML = "›";
        nextBtn.style.position = "absolute";
        nextBtn.style.right = "10px";
        nextBtn.style.top = "50%";
        nextBtn.style.transform = "translateY(-50%)";
        nextBtn.style.backgroundColor = "rgba(0,0,0,0.5)";
        nextBtn.style.color = "white";
        nextBtn.style.border = "none";
        nextBtn.style.borderRadius = "50%";
        nextBtn.style.width = "40px";
        nextBtn.style.height = "40px";
        nextBtn.style.cursor = "pointer";
        nextBtn.style.fontSize = "18px";
        nextBtn.style.zIndex = "10";
        
        nextBtn.addEventListener("click", () => {
            currentIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
            updateCarousel();
        });
        
        // Create indicators
        const indicators = document.createElement("div");
        indicators.className = "carousel-indicators";
        indicators.style.position = "absolute";
        indicators.style.bottom = "10px";
        indicators.style.left = "50%";
        indicators.style.transform = "translateX(-50%)";
        indicators.style.display = "flex";
        indicators.style.gap = "8px";
        indicators.style.zIndex = "10";
        
        items.forEach((_, index) => {
            const indicator = document.createElement("button");
            indicator.className = "carousel-indicator";
            indicator.style.width = "10px";
            indicator.style.height = "10px";
            indicator.style.borderRadius = "50%";
            indicator.style.border = "none";
            indicator.style.backgroundColor = index === 0 ? "#007bff" : "#ccc";
            indicator.style.cursor = "pointer";
            
            indicator.addEventListener("click", () => {
                currentIndex = index;
                updateCarousel();
            });
            
            indicators.appendChild(indicator);
        });
        
        el.appendChild(prevBtn);
        el.appendChild(nextBtn);
        el.appendChild(indicators);
    }
    
    el.appendChild(itemsContainer);
    
    return el;
}