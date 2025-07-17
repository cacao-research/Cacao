/*
 * Auto-generated Cacao Components
 * Generated on: 2025-07-17 01:02:00
 * Components: 36
 *
 * This file extends window.CacaoCore.componentRenderers with compiled components.
 * It must be loaded AFTER cacao-core.js to ensure the global registry exists.
 */


// Auto-generated component: _template
(function(){
    try {
        const _templateRenderer = // Template for creating new Cacao components
// Copy this file to your component directory and modify as needed

// Component renderer function
(component) => {
    // Create the main element
    const el = document.createElement("div");
    el.className = "your-component-name";
    
    // Handle component props
    if (component.props?.className) {
        el.className += " " + component.props.className;
    }
    
    if (component.props?.style) {
        Object.assign(el.style, component.props.style);
    }
    
    // Handle component content
    if (component.props?.content) {
        // This will be auto-transformed to window.CacaoCore.applyContent()
        window.CacaoCore.applyContent(el, component.props.content);
    }
    
    // Handle component children
    if (component.children) {
        // This will be auto-transformed to window.CacaoCore.renderChildren()
        window.CacaoCore.renderChildren(el, component.children);
    } else if (component.props?.children) {
        // This will be auto-transformed to window.CacaoCore.renderChildren()
        window.CacaoCore.renderChildren(el, component.props.children);
    }
    
    // Handle nested components
    if (component.props?.nestedComponent) {
        // This will be auto-transformed to window.CacaoCore.renderComponent()
        const nestedEl = window.CacaoCore.renderComponent(component.props.nestedComponent);
        el.appendChild(nestedEl);
    }
    
    // Add event listeners if needed
    if (component.props?.onClick) {
        el.addEventListener('click', component.props.onClick);
    }
    
    // Return the completed element
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['_template'] = _templateRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: _template', error);
    }
})();

// Auto-generated component: avatar
(function(){
    try {
        const avatarRenderer = (component) => {
    console.log("[CacaoCore] Rendering avatar component:", component);
    const el = document.createElement("span");
    el.className = "avatar";
    
    if (component.props.shape) {
        el.classList.add(component.props.shape);
    }
    if (component.props.size) {
        el.classList.add(component.props.size);
    }

    if (component.props.src) {
        const img = document.createElement("img");
        img.src = component.props.src;
        img.alt = "Avatar";
        el.appendChild(img);
    } else if (component.props.icon) {
        const icon = document.createElement("span");
        icon.className = "avatar-icon";
        window.CacaoCore.applyContent(icon, component.props.icon);
        el.appendChild(icon);
    }

    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['avatar'] = avatarRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: avatar', error);
    }
})();

// Auto-generated component: badge
(function(){
    try {
        const badgeRenderer = (component) => {
    console.log("[CacaoCore] Rendering badge component:", component);
    const wrapper = document.createElement("span");
    wrapper.className = "badge-wrapper";

    // Render the main content if provided
    if (component.props.children) {
        wrapper.appendChild(window.CacaoCore.renderComponent(component.props.children));
    }

    // Create the badge element
    const badge = document.createElement("span");
    badge.className = "badge";

    // Handle dot style badge
    if (component.props.dot) {
        badge.classList.add("dot");
    } else if (component.props.count !== undefined) {
        // Show count if not zero or showZero is true
        if (component.props.count > 0 || component.props.showZero) {
            badge.textContent = component.props.count;
        }
    }

    wrapper.appendChild(badge);
    return wrapper;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['badge'] = badgeRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: badge', error);
    }
})();

// Auto-generated component: card
(function(){
    try {
        const cardRenderer = (component) => {
    console.log("[CacaoCore] Rendering card component:", component);
    const el = document.createElement("div");
    el.className = "card";
    if (component.props.bordered) el.classList.add("bordered");

    if (component.props.title) {
        const header = document.createElement("div");
        header.className = "card-header";
        const title = document.createElement("div");
        title.className = "card-title";
        title.textContent = component.props.title;
        header.appendChild(title);

        if (component.props.extra) {
            const extra = document.createElement("div");
            extra.className = "card-extra";
            if (typeof component.props.extra === 'string') {
                extra.textContent = component.props.extra;
            } else {
                extra.appendChild(window.CacaoCore.renderComponent(component.props.extra));
            }
            header.appendChild(extra);
        }

        el.appendChild(header);
    }

    const content = document.createElement("div");
    content.className = "card-content";
    if (typeof component.props.children === 'string') {
        content.textContent = component.props.children;
    } else if (Array.isArray(component.props.children)) {
        component.props.children.forEach(child => {
            content.appendChild(window.CacaoCore.renderComponent(child));
        });
    } else if (component.props.children) {
        content.appendChild(window.CacaoCore.renderComponent(component.props.children));
    }
    el.appendChild(content);

    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['card'] = cardRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: card', error);
    }
})();

// Auto-generated component: carousel
(function(){
    try {
        const carouselRenderer = (component) => {
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
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['carousel'] = carouselRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: carousel', error);
    }
})();

// Auto-generated component: collapse
(function(){
    try {
        const collapseRenderer = (component) => {
    console.log("[CacaoCore] Rendering collapse component:", component);
    
    // Create main element
    const el = document.createElement("div");
    el.className = "collapse";
    el.style.border = "1px solid #ddd";
    el.style.borderRadius = "4px";
    el.style.marginBottom = "8px";
    
    // Track collapse state
    let isCollapsed = component.props.defaultCollapsed !== false;
    
    // Create header (trigger)
    const header = document.createElement("div");
    header.className = "collapse-header";
    header.style.padding = "12px 16px";
    header.style.backgroundColor = "#f8f9fa";
    header.style.borderBottom = "1px solid #ddd";
    header.style.cursor = "pointer";
    header.style.display = "flex";
    header.style.alignItems = "center";
    header.style.justifyContent = "space-between";
    header.style.userSelect = "none";
    
    // Add header title
    const headerTitle = document.createElement("div");
    headerTitle.className = "collapse-title";
    headerTitle.style.fontWeight = "500";
    headerTitle.textContent = component.props.title || "Collapse";
    header.appendChild(headerTitle);
    
    // Add collapse indicator
    const indicator = document.createElement("div");
    indicator.className = "collapse-indicator";
    indicator.style.fontSize = "12px";
    indicator.style.transition = "transform 0.2s ease";
    indicator.innerHTML = "▼";
    header.appendChild(indicator);
    
    // Create content area
    const content = document.createElement("div");
    content.className = "collapse-content";
    content.style.overflow = "hidden";
    content.style.transition = "max-height 0.3s ease, opacity 0.3s ease";
    
    // Create content wrapper
    const contentWrapper = document.createElement("div");
    contentWrapper.className = "collapse-content-wrapper";
    contentWrapper.style.padding = "16px";
    
    // Add content
    if (component.props.children) {
        if (typeof component.props.children === 'string') {
            contentWrapper.textContent = component.props.children;
        } else if (Array.isArray(component.props.children)) {
            component.props.children.forEach(child => {
                contentWrapper.appendChild(window.CacaoCore.renderComponent(child));
            });
        } else {
            contentWrapper.appendChild(window.CacaoCore.renderComponent(component.props.children));
        }
    } else {
        contentWrapper.innerHTML = `
            <div style="color: #666; font-style: italic;">
                Collapse content goes here...
            </div>
        `;
    }
    
    content.appendChild(contentWrapper);
    
    // Function to update collapse state
    const updateCollapse = () => {
        if (isCollapsed) {
            content.style.maxHeight = "0";
            content.style.opacity = "0";
            content.style.borderTop = "none";
            indicator.style.transform = "rotate(-90deg)";
        } else {
            content.style.maxHeight = contentWrapper.scrollHeight + "px";
            content.style.opacity = "1";
            content.style.borderTop = "1px solid #ddd";
            indicator.style.transform = "rotate(0deg)";
        }
    };
    
    // Add click handler to header
    header.addEventListener("click", () => {
        isCollapsed = !isCollapsed;
        updateCollapse();
    });
    
    // Add keyboard support
    header.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            isCollapsed = !isCollapsed;
            updateCollapse();
        }
    });
    
    // Make header focusable
    header.setAttribute("tabindex", "0");
    header.setAttribute("role", "button");
    header.setAttribute("aria-expanded", !isCollapsed);
    
    // Add hover effect
    header.addEventListener("mouseenter", () => {
        header.style.backgroundColor = "#e9ecef";
    });
    
    header.addEventListener("mouseleave", () => {
        header.style.backgroundColor = "#f8f9fa";
    });
    
    // Assemble component
    el.appendChild(header);
    el.appendChild(content);
    
    // Set initial state
    updateCollapse();
    
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['collapse'] = collapseRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: collapse', error);
    }
})();

// Auto-generated component: descriptions
(function(){
    try {
        const descriptionsRenderer = (component) => {
    console.log("[CacaoCore] Rendering descriptions component:", component);
    const el = document.createElement("div");
    el.className = "descriptions";
    
    // Add bordered class if specified
    if (component.props.bordered) {
        el.classList.add("bordered");
    }

    // Add columns class if specified
    if (component.props.column) {
        el.classList.add(`columns-${component.props.column}`);
    }

    // Add title if provided
    if (component.props.title) {
        const titleDiv = document.createElement("div");
        titleDiv.className = "descriptions-title";
        titleDiv.textContent = component.props.title;
        el.appendChild(titleDiv);
    }

    // Create items wrapper
    const itemsWrapper = document.createElement("div");
    itemsWrapper.className = "descriptions-items";

    // Add items
    if (Array.isArray(component.props.items)) {
        component.props.items.forEach(item => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "descriptions-item";

            const labelDiv = document.createElement("div");
            labelDiv.className = "descriptions-label";
            labelDiv.textContent = item.label;
            itemDiv.appendChild(labelDiv);

            const contentDiv = document.createElement("div");
            contentDiv.className = "descriptions-content";
            if (typeof item.content === 'string') {
                contentDiv.textContent = item.content;
            } else {
                contentDiv.appendChild(window.CacaoCore.renderComponent(item.content));
            }
            itemDiv.appendChild(contentDiv);

            itemsWrapper.appendChild(itemDiv);
        });
    }

    el.appendChild(itemsWrapper);

    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .descriptions {
            width: 100%;
            font-size: 14px;
        }

        .descriptions.bordered {
            border: 1px solid #e8e8e8;
            border-radius: 4px;
        }

        .descriptions-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            padding: 16px;
            border-bottom: 1px solid #e8e8e8;
        }

        .descriptions-items {
            padding: 16px;
            display: grid;
            grid-gap: 16px;
        }

        .descriptions.columns-2 .descriptions-items {
            grid-template-columns: repeat(2, 1fr);
        }

        .descriptions-item {
            display: flex;
            flex-direction: column;
        }

        .descriptions-label {
            color: #666;
            margin-bottom: 4px;
        }

        .descriptions-content {
            color: #333;
        }

        .descriptions.bordered .descriptions-items {
            border-radius: 0 0 4px 4px;
        }
    `;
    el.appendChild(style);

    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['descriptions'] = descriptionsRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: descriptions', error);
    }
})();

// Auto-generated component: image
(function(){
    try {
        const imageRenderer = (component) => {
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
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['image'] = imageRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: image', error);
    }
})();

// Auto-generated component: list
(function(){
    try {
        const listRenderer = (component) => {
    console.log("[CacaoCore] Rendering list component:", component);
    const el = document.createElement("div");
    el.className = "list";
    if (component.props.bordered) el.classList.add("bordered");
    if (component.props.size) el.classList.add(component.props.size);

    if (Array.isArray(component.props.items)) {
        component.props.items.forEach(item => {
            const itemEl = document.createElement("div");
            itemEl.className = "list-item";
            
            if (item.title) {
                const title = document.createElement("div");
                title.className = "list-item-title";
                title.textContent = item.title;
                itemEl.appendChild(title);
            }

            if (item.description) {
                const desc = document.createElement("div");
                desc.className = "list-item-description";
                desc.textContent = item.description;
                itemEl.appendChild(desc);
            }

            el.appendChild(itemEl);
        });
    }

    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['list'] = listRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: list', error);
    }
})();

// Auto-generated component: plot
(function(){
    try {
        const plotRenderer = (component) => {
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
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['plot'] = plotRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: plot', error);
    }
})();

// Auto-generated component: popover
(function(){
    try {
        const popoverRenderer = (component) => {
    console.log("[CacaoCore] Rendering popover component:", component);
    
    // Create main wrapper element
    const wrapper = document.createElement("div");
    wrapper.className = "popover-wrapper";
    wrapper.style.position = "relative";
    wrapper.style.display = "inline-block";
    
    // Render the trigger element
    const trigger = document.createElement("span");
    trigger.className = "popover-trigger";
    trigger.style.cursor = "pointer";
    
    if (component.props.children) {
        if (typeof component.props.children === 'string') {
            trigger.textContent = component.props.children;
        } else {
            trigger.appendChild(window.CacaoCore.renderComponent(component.props.children));
        }
    } else {
        trigger.textContent = "Click me";
    }
    
    // Create popover element
    const popover = document.createElement("div");
    popover.className = "popover";
    popover.style.position = "absolute";
    popover.style.backgroundColor = "white";
    popover.style.border = "1px solid #ccc";
    popover.style.borderRadius = "4px";
    popover.style.boxShadow = "0 2px 8px rgba(0,0,0,0.15)";
    popover.style.padding = "12px";
    popover.style.minWidth = "200px";
    popover.style.maxWidth = "300px";
    popover.style.zIndex = "1000";
    popover.style.display = "none";
    
    // Add popover content
    const content = document.createElement("div");
    content.className = "popover-content";
    
    if (component.props.title) {
        const title = document.createElement("div");
        title.className = "popover-title";
        title.style.fontWeight = "bold";
        title.style.marginBottom = "8px";
        title.textContent = component.props.title;
        content.appendChild(title);
    }
    
    if (component.props.content) {
        const body = document.createElement("div");
        body.className = "popover-body";
        if (typeof component.props.content === 'string') {
            body.textContent = component.props.content;
        } else {
            body.appendChild(window.CacaoCore.renderComponent(component.props.content));
        }
        content.appendChild(body);
    }
    
    popover.appendChild(content);
    
    // Position popover based on placement
    const placement = component.props.placement || "bottom";
    switch (placement) {
        case "top":
            popover.style.bottom = "100%";
            popover.style.left = "50%";
            popover.style.transform = "translateX(-50%)";
            popover.style.marginBottom = "8px";
            break;
        case "bottom":
            popover.style.top = "100%";
            popover.style.left = "50%";
            popover.style.transform = "translateX(-50%)";
            popover.style.marginTop = "8px";
            break;
        case "left":
            popover.style.right = "100%";
            popover.style.top = "50%";
            popover.style.transform = "translateY(-50%)";
            popover.style.marginRight = "8px";
            break;
        case "right":
            popover.style.left = "100%";
            popover.style.top = "50%";
            popover.style.transform = "translateY(-50%)";
            popover.style.marginLeft = "8px";
            break;
    }
    
    // Add click handler to toggle popover
    let isVisible = false;
    trigger.addEventListener("click", (e) => {
        e.stopPropagation();
        isVisible = !isVisible;
        popover.style.display = isVisible ? "block" : "none";
    });
    
    // Hide popover when clicking outside
    document.addEventListener("click", (e) => {
        if (!wrapper.contains(e.target) && isVisible) {
            isVisible = false;
            popover.style.display = "none";
        }
    });
    
    wrapper.appendChild(trigger);
    wrapper.appendChild(popover);
    
    return wrapper;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['popover'] = popoverRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: popover', error);
    }
})();

// Auto-generated component: table
(function(){
    try {
        const tableRenderer = (component) => {
    console.log("[CacaoCore] Rendering enhanced table component:", component);
    const wrapper = document.createElement("div");
    wrapper.className = "table-wrapper";

    const table = document.createElement("table");
    table.className = "table";

    // Create header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    component.props.columns.forEach(column => {
        const th = document.createElement("th");
        th.textContent = column.title;
        if (component.props.sorting) {
            th.classList.add("sortable");
            th.onclick = () => {
                // Sorting logic would go here
                console.log("[CacaoCore] Sort by:", column.key);
            };
        }
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create body
    const tbody = document.createElement("tbody");
    if (Array.isArray(component.props.dataSource)) {
        component.props.dataSource.forEach(row => {
            const tr = document.createElement("tr");
            component.props.columns.forEach(column => {
                const td = document.createElement("td");
                td.textContent = row[column.dataIndex];
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }
    table.appendChild(tbody);

    wrapper.appendChild(table);

    // Add pagination if specified
    if (component.props.pagination) {
        const pagination = document.createElement("div");
        pagination.className = "table-pagination";
        // Pagination UI would go here
        wrapper.appendChild(pagination);
    }

    return wrapper;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['table'] = tableRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: table', error);
    }
})();

// Auto-generated component: tag
(function(){
    try {
        const tagRenderer = (component) => {
    console.log("[CacaoCore] Rendering tag component:", component);
    const el = document.createElement("span");
    el.className = "tag";
    
    if (component.props.color) {
        el.classList.add(`tag-${component.props.color}`);
        el.style.backgroundColor = component.props.color;
    }

    if (component.props.content) {
        el.textContent = component.props.content;
    }

    if (component.props.closable) {
        const closeBtn = document.createElement("span");
        closeBtn.className = "tag-close";
        closeBtn.innerHTML = "×";
        closeBtn.onclick = (e) => {
            e.stopPropagation();
            el.remove();
        };
        el.appendChild(closeBtn);
    }

    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['tag'] = tagRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: tag', error);
    }
})();

// Auto-generated component: timeline
(function(){
    try {
        const timelineRenderer = (component) => {
    console.log("[CacaoCore] Rendering timeline component:", component);
    const el = document.createElement("div");
    el.className = "timeline";
    
    if (component.props.mode) {
        el.classList.add(`timeline-${component.props.mode}`);
    }
    
    if (component.props.reverse) {
        el.classList.add("timeline-reverse");
    }

    if (Array.isArray(component.props.items)) {
        const items = component.props.reverse ?
            [...component.props.items].reverse() :
            component.props.items;
            
        items.forEach(item => {
            const itemEl = document.createElement("div");
            itemEl.className = "timeline-item";

            // Add dot
            const dot = document.createElement("div");
            dot.className = "timeline-dot";
            itemEl.appendChild(dot);

            // Add label if provided
            if (item.label) {
                const label = document.createElement("div");
                label.className = "timeline-label";
                label.textContent = item.label;
                itemEl.appendChild(label);
            }

            // Add content
            const content = document.createElement("div");
            content.className = "timeline-content";
            if (typeof item.content === 'string') {
                content.textContent = item.content;
            } else {
                content.appendChild(window.CacaoCore.renderComponent(item.content));
            }
            itemEl.appendChild(content);

            el.appendChild(itemEl);
        });
    }

    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['timeline'] = timelineRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: timeline', error);
    }
})();

// Auto-generated component: tooltip
(function(){
    try {
        const tooltipRenderer = (component) => {
    console.log("[CacaoCore] Rendering tooltip component:", component);
    
    // Create main wrapper element
    const wrapper = document.createElement("div");
    wrapper.className = "tooltip-wrapper";
    wrapper.style.position = "relative";
    wrapper.style.display = "inline-block";
    
    // Render the main content (trigger element)
    if (component.props.children) {
        if (typeof component.props.children === 'string') {
            wrapper.textContent = component.props.children;
        } else {
            wrapper.appendChild(window.CacaoCore.renderComponent(component.props.children));
        }
    }
    
    // Create tooltip element
    const tooltip = document.createElement("div");
    tooltip.className = "tooltip";
    tooltip.style.position = "absolute";
    tooltip.style.backgroundColor = "#333";
    tooltip.style.color = "white";
    tooltip.style.padding = "8px 12px";
    tooltip.style.borderRadius = "4px";
    tooltip.style.fontSize = "12px";
    tooltip.style.whiteSpace = "nowrap";
    tooltip.style.zIndex = "1000";
    tooltip.style.opacity = "0";
    tooltip.style.visibility = "hidden";
    tooltip.style.transition = "opacity 0.3s, visibility 0.3s";
    tooltip.style.pointerEvents = "none";
    
    // Set tooltip content
    tooltip.textContent = component.props.title || component.props.content || "Tooltip";
    
    // Position tooltip based on placement
    const placement = component.props.placement || "top";
    switch (placement) {
        case "top":
            tooltip.style.bottom = "100%";
            tooltip.style.left = "50%";
            tooltip.style.transform = "translateX(-50%)";
            tooltip.style.marginBottom = "8px";
            break;
        case "bottom":
            tooltip.style.top = "100%";
            tooltip.style.left = "50%";
            tooltip.style.transform = "translateX(-50%)";
            tooltip.style.marginTop = "8px";
            break;
        case "left":
            tooltip.style.right = "100%";
            tooltip.style.top = "50%";
            tooltip.style.transform = "translateY(-50%)";
            tooltip.style.marginRight = "8px";
            break;
        case "right":
            tooltip.style.left = "100%";
            tooltip.style.top = "50%";
            tooltip.style.transform = "translateY(-50%)";
            tooltip.style.marginLeft = "8px";
            break;
    }
    
    // Add event listeners for hover
    wrapper.addEventListener("mouseenter", () => {
        tooltip.style.opacity = "1";
        tooltip.style.visibility = "visible";
    });
    
    wrapper.addEventListener("mouseleave", () => {
        tooltip.style.opacity = "0";
        tooltip.style.visibility = "hidden";
    });
    
    wrapper.appendChild(tooltip);
    
    return wrapper;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['tooltip'] = tooltipRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: tooltip', error);
    }
})();

// Auto-generated component: checkbox
(function(){
    try {
        const checkboxRenderer = // Checkbox component renderer
(component) => {
    const wrapper = document.createElement("label");
    wrapper.className = "checkbox-wrapper";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = !!component.props.checked;
    if (component.props.disabled) input.disabled = true;
    if (component.props.style) Object.assign(input.style, component.props.style);
    if (component.props.className) input.className = component.props.className;
    wrapper.appendChild(input);
    if (component.props.label) {
        const span = document.createElement("span");
        span.textContent = component.props.label;
        wrapper.appendChild(span);
    }
    return wrapper;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['checkbox'] = checkboxRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: checkbox', error);
    }
})();

// Auto-generated component: datepicker
(function(){
    try {
        const datepickerRenderer = // Datepicker Component Renderer
(component) => {
    const el = document.createElement("input");
    el.type = "date";
    if (component.props.value) el.value = component.props.value;
    if (component.props.disabled) el.disabled = true;
    if (component.props.style) Object.assign(el.style, component.props.style);
    if (component.props.className) el.className = component.props.className;
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['datepicker'] = datepickerRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: datepicker', error);
    }
})();

// Auto-generated component: input
(function(){
    try {
        const inputRenderer = // Input Component Renderer
(component) => {
    const el = document.createElement("input");
    el.type = component.props.inputType || "text";
    el.value = component.props.value || "";
    if (component.props.placeholder) el.placeholder = component.props.placeholder;
    if (component.props.disabled) el.disabled = true;
    if (component.props.style) Object.assign(el.style, component.props.style);
    if (component.props.className) el.className = component.props.className;
    // No onChange binding by default (add if needed)
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['input'] = inputRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: input', error);
    }
})();

// Auto-generated component: radio
(function(){
    try {
        const radioRenderer = // Radio component renderer
(component) => {
    const wrapper = document.createElement("div");
    wrapper.className = "radio-group";
    if (Array.isArray(component.props.options)) {
        component.props.options.forEach(opt => {
            const label = document.createElement("label");
            label.className = "radio-wrapper";
            const input = document.createElement("input");
            input.type = "radio";
            input.name = "radio-group-" + Math.random().toString(36).substr(2, 6);
            input.value = opt.value;
            if (component.props.value === opt.value) input.checked = true;
            if (component.props.disabled) input.disabled = true;
            label.appendChild(input);
            const span = document.createElement("span");
            span.textContent = opt.label;
            label.appendChild(span);
            wrapper.appendChild(label);
        });
    }
    return wrapper;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['radio'] = radioRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: radio', error);
    }
})();

// Auto-generated component: range-sliders
(function(){
    try {
        const rangeSlidersRenderer = /**
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
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['range-sliders'] = rangeSlidersRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: range-sliders', error);
    }
})();

// Auto-generated component: rate
(function(){
    try {
        const rateRenderer = // Rate Component Renderer
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
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['rate'] = rateRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: rate', error);
    }
})();

// Auto-generated component: search
(function(){
    try {
        const searchRenderer = // Search Component Renderer
(component) => {
    // Render as input[type=search] + button (or just input)
    const wrapper = document.createElement("div");
    wrapper.className = "search-input-wrapper";
    const input = document.createElement("input");
    input.type = "search";
    input.value = component.props.value || "";
    if (component.props.placeholder) input.placeholder = component.props.placeholder;
    if (component.props.disabled) input.disabled = true;
    if (component.props.style) Object.assign(input.style, component.props.style);
    if (component.props.className) input.className = component.props.className;
    wrapper.appendChild(input);
    // Optionally add a search button
    // const button = document.createElement("button");
    // button.textContent = "Search";
    // wrapper.appendChild(button);
    return wrapper;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['search'] = searchRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: search', error);
    }
})();

// Auto-generated component: select
(function(){
    try {
        const selectRenderer = // Select Component Renderer
(component) => {
    const el = document.createElement("select");
    if (component.props.disabled) el.disabled = true;
    if (component.props.style) Object.assign(el.style, component.props.style);
    if (component.props.className) el.className = component.props.className;
    if (component.props.placeholder) {
        const placeholderOption = document.createElement("option");
        placeholderOption.value = "";
        placeholderOption.disabled = true;
        placeholderOption.selected = !component.props.value;
        placeholderOption.hidden = true;
        placeholderOption.textContent = component.props.placeholder;
        el.appendChild(placeholderOption);
    }
    if (Array.isArray(component.props.options)) {
        component.props.options.forEach(opt => {
            const option = document.createElement("option");
            option.value = opt.value;
            option.textContent = opt.label;
            if (component.props.value === opt.value) option.selected = true;
            el.appendChild(option);
        });
    }
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['select'] = selectRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: select', error);
    }
})();

// Auto-generated component: slider
(function(){
    try {
        const sliderRenderer = // Slider Component Renderer
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
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['slider'] = sliderRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: slider', error);
    }
})();

// Auto-generated component: switch
(function(){
    try {
        const switchRenderer = // Switch component renderer
(component) => {
    // Styled checkbox
    const wrapper = document.createElement("label");
    wrapper.className = "switch-wrapper";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = !!component.props.checked;
    if (component.props.disabled) input.disabled = true;
    if (component.props.className) input.className = component.props.className;
    wrapper.appendChild(input);
    const slider = document.createElement("span");
    slider.className = "switch-slider";
    wrapper.appendChild(slider);
    return wrapper;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['switch'] = switchRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: switch', error);
    }
})();

// Auto-generated component: textarea
(function(){
    try {
        const textareaRenderer = // Textarea Component Renderer
(component) => {
    const el = document.createElement("textarea");
    el.className = component.props.className || "textarea";
    
    // Apply content
    if (component.props.content) {
        el.value = component.props.content;
    }
    
    // Apply styles
    if (component.props.style) {
        Object.assign(el.style, component.props.style);
    }
    
    // Handle content changes
    if (component.props.action) {
        let updateTimeout;
        
        el.addEventListener("input", () => {
            // Clear any existing timeout to debounce
            clearTimeout(updateTimeout);
            
            // Set a timeout to avoid sending too many events
            updateTimeout = setTimeout(async () => {
                try {
                    const action = component.props.action;
                    const componentType = component.component_type || "textarea";
                    
                    // Build event data including the textarea content
                    const eventData = {
                        component_type: componentType,
                        content: el.value
                    };
                    
                    // Add the data property from the component if it exists
                    if (component.props.data) {
                        console.log("[Cacao] Including custom data in textarea event:", component.props.data);
                        Object.assign(eventData, component.props.data);
                    }
                    
                    console.log("[Cacao] Sending textarea content update:", action, eventData);
                    
                    // If WebSocket is open
                    if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
                        window.socket.send(JSON.stringify({
                            type: 'event',
                            event: action,
                            data: eventData
                        }));
                    } else {
                        // Fallback to HTTP
                        console.log("[Cacao] WebSocket not available, using HTTP fallback for textarea");
                        
                        // Build query parameters
                        let queryParams = `action=${action}&component_type=${componentType}`;
                        
                        // Add the data property from the component if it exists
                        if (component.props.data) {
                            for (const [key, value] of Object.entries(component.props.data)) {
                                queryParams += `&${key}=${encodeURIComponent(value)}`;
                            }
                        }
                        
                        // Add content parameter
                        queryParams += `&content=${encodeURIComponent(el.value)}`;
                        
                        const response = await fetch(`/api/action?${queryParams}&t=${Date.now()}`, {
                            method: 'GET',
                            headers: {
                                'Cache-Control': 'no-cache, no-store, must-revalidate',
                                'Pragma': 'no-cache',
                                'Expires': '0'
                            }
                        });
                        
                        if (!response.ok) {
                            const errorText = await response.text();
                            console.error("[Cacao] Server error response:", errorText);
                            throw new Error(`Server returned ${response.status}: ${errorText}`);
                        }
                        
                        const responseData = await response.json();
                        console.log("[CacaoCore] Server response data:", responseData);
                    }
                } catch (err) {
                    console.error('[CacaoCore] Error handling textarea input:', err);
                }
            }, 1000); // 1 second debounce
        });
    }
    
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['textarea'] = textareaRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: textarea', error);
    }
})();

// Auto-generated component: timepicker
(function(){
    try {
        const timepickerRenderer = // Timepicker Component Renderer
(component) => {
    const el = document.createElement("input");
    el.type = "time";
    if (component.props.value) el.value = component.props.value;
    if (component.props.disabled) el.disabled = true;
    if (component.props.style) Object.assign(el.style, component.props.style);
    if (component.props.className) el.className = component.props.className;
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['timepicker'] = timepickerRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: timepicker', error);
    }
})();

// Auto-generated component: upload
(function(){
    try {
        const uploadRenderer = // Upload Component Renderer
(component) => {
    const wrapper = document.createElement("div");
    wrapper.className = "upload-wrapper";
    const input = document.createElement("input");
    input.type = "file";
    if (component.props.multiple) input.multiple = true;
    if (component.props.disabled) input.disabled = true;
    if (component.props.style) Object.assign(input.style, component.props.style);
    if (component.props.className) input.className = component.props.className;
    wrapper.appendChild(input);
    return wrapper;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['upload'] = uploadRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: upload', error);
    }
})();

// Auto-generated component: menu
(function(){
    try {
        const menuRenderer = /**
 * Menu Component JavaScript
 * Handles menu rendering, navigation, and interactions
 */

class MenuRenderer {
    constructor(containerId, props = {}) {
        this.containerId = containerId;
        this.props = props;
        this.menuElement = null;
        this.openSubmenus = new Set();
        this.focusedItem = null;
        this.keydownHandler = null;
        
        this.init();
    }

    init() {
        this.render();
        this.setupEventListeners();
        this.setupKeyboardNavigation();
    }

    render() {
        const container = document.getElementById(this.containerId);
        if (!container) return;

        const menu = this.createMenu();
        container.innerHTML = '';
        container.appendChild(menu);
        
        this.menuElement = menu;
    }

    createMenu() {
        const menu = document.createElement('ul');
        menu.className = this.getMenuClasses();
        menu.setAttribute('role', 'menu');
        menu.setAttribute('aria-orientation', this.props.orientation || 'vertical');

        if (this.props.items && this.props.items.length > 0) {
            this.props.items.forEach(item => {
                const menuItem = this.createMenuItem(item);
                menu.appendChild(menuItem);
            });
        }

        return menu;
    }

    createMenuItem(item) {
        const listItem = document.createElement('li');
        listItem.className = this.getMenuItemClasses(item);
        listItem.setAttribute('role', 'none');

        if (item.children && item.children.length > 0) {
            // Create submenu
            const submenuToggle = this.createSubmenuToggle(item);
            const submenu = this.createSubmenu(item);
            
            listItem.appendChild(submenuToggle);
            listItem.appendChild(submenu);
        } else {
            // Create regular menu item
            const menuLink = this.createMenuLink(item);
            listItem.appendChild(menuLink);
        }

        return listItem;
    }

    createMenuLink(item) {
        const element = document.createElement(item.url ? 'a' : 'button');
        element.className = 'menu-link';
        element.setAttribute('role', 'menuitem');
        element.setAttribute('tabindex', '-1');

        if (item.url) {
            element.href = item.url;
        } else {
            element.type = 'button';
        }

        if (item.disabled) {
            element.setAttribute('aria-disabled', 'true');
            element.setAttribute('disabled', 'true');
        }

        if (item.active) {
            element.setAttribute('aria-current', 'page');
        }

        // Create link content
        const linkContent = document.createElement('div');
        linkContent.className = 'menu-link-content';

        // Add icon if present
        if (item.icon) {
            const icon = document.createElement('i');
            icon.className = `menu-icon ${item.icon}`;
            linkContent.appendChild(icon);
        }

        // Add label
        const label = document.createElement('span');
        label.className = 'menu-label';
        label.textContent = item.label;
        linkContent.appendChild(label);

        // Add badge if present
        if (item.badge !== undefined && item.badge !== null) {
            const badge = document.createElement('span');
            badge.className = 'menu-badge';
            badge.textContent = item.badge;
            linkContent.appendChild(badge);
        }

        element.appendChild(linkContent);

        // Add click handler
        element.addEventListener('click', (e) => {
            this.handleItemClick(e, item);
        });

        return element;
    }

    createSubmenuToggle(item) {
        const button = document.createElement('button');
        button.className = 'menu-submenu-toggle';
        button.setAttribute('role', 'menuitem');
        button.setAttribute('aria-haspopup', 'true');
        button.setAttribute('aria-expanded', 'false');
        button.setAttribute('tabindex', '-1');

        if (item.disabled) {
            button.setAttribute('aria-disabled', 'true');
            button.setAttribute('disabled', 'true');
        }

        // Create toggle content
        const toggleContent = document.createElement('div');
        toggleContent.className = 'menu-submenu-toggle-content';

        // Add icon if present
        if (item.icon) {
            const icon = document.createElement('i');
            icon.className = `menu-icon ${item.icon}`;
            toggleContent.appendChild(icon);
        }

        // Add label
        const label = document.createElement('span');
        label.className = 'menu-label';
        label.textContent = item.label;
        toggleContent.appendChild(label);

        // Add badge if present
        if (item.badge !== undefined && item.badge !== null) {
            const badge = document.createElement('span');
            badge.className = 'menu-badge';
            badge.textContent = item.badge;
            toggleContent.appendChild(badge);
        }

        // Add arrow
        const arrow = document.createElement('i');
        arrow.className = 'menu-arrow';
        toggleContent.appendChild(arrow);

        button.appendChild(toggleContent);

        // Add click handler
        button.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleSubmenu(item.key, button);
        });

        return button;
    }

    createSubmenu(item) {
        const submenu = document.createElement('ul');
        submenu.className = 'menu-submenu';
        submenu.setAttribute('role', 'menu');
        submenu.setAttribute('aria-labelledby', item.key);

        if (item.children && item.children.length > 0) {
            item.children.forEach(child => {
                const childItem = this.createMenuItem(child);
                submenu.appendChild(childItem);
            });
        }

        return submenu;
    }

    getMenuClasses() {
        let classes = 'menu';

        if (this.props.orientation) {
            classes += ` menu-${this.props.orientation}`;
        }

        if (this.props.size) {
            classes += ` menu-${this.props.size}`;
        }

        if (this.props.variant) {
            classes += ` menu-${this.props.variant}`;
        }

        if (this.props.theme) {
            classes += ` menu-${this.props.theme}`;
        }

        if (this.props.collapsed) {
            classes += ' menu-collapsed';
        }

        return classes;
    }

    getMenuItemClasses(item) {
        let classes = 'menu-item';

        if (item.active) {
            classes += ' menu-item-active';
        }

        if (item.disabled) {
            classes += ' menu-item-disabled';
        }

        if (item.children && item.children.length > 0) {
            classes += ' menu-item-submenu';
            
            if (this.openSubmenus.has(item.key)) {
                classes += ' menu-item-submenu-open';
            }
        }

        return classes;
    }

    toggleSubmenu(key, button) {
        if (this.openSubmenus.has(key)) {
            this.closeSubmenu(key, button);
        } else {
            this.openSubmenu(key, button);
        }
    }

    openSubmenu(key, button) {
        this.openSubmenus.add(key);
        button.setAttribute('aria-expanded', 'true');
        button.parentElement.classList.add('menu-item-submenu-open');
    }

    closeSubmenu(key, button) {
        this.openSubmenus.delete(key);
        button.setAttribute('aria-expanded', 'false');
        button.parentElement.classList.remove('menu-item-submenu-open');
    }

    handleItemClick(event, item) {
        if (item.disabled) {
            event.preventDefault();
            return;
        }

        // Call click callback if provided
        if (this.props.on_click) {
            this.callCallback(this.props.on_click, { item, event });
        }

        // Handle active state
        if (!item.url) {
            event.preventDefault();
            this.setActiveItem(item.key);
        }
    }

    setActiveItem(key) {
        // Remove active class from all items
        const activeItems = this.menuElement.querySelectorAll('.menu-item-active');
        activeItems.forEach(item => {
            item.classList.remove('menu-item-active');
            const link = item.querySelector('.menu-link, .menu-submenu-toggle');
            if (link) {
                link.removeAttribute('aria-current');
            }
        });

        // Add active class to selected item
        const items = this.menuElement.querySelectorAll('.menu-item');
        items.forEach(item => {
            const link = item.querySelector('.menu-link, .menu-submenu-toggle');
            if (link && this.getItemKey(item) === key) {
                item.classList.add('menu-item-active');
                link.setAttribute('aria-current', 'page');
            }
        });
    }

    getItemKey(element) {
        // Extract key from the data or generate from content
        const link = element.querySelector('.menu-link, .menu-submenu-toggle');
        if (link) {
            const label = link.querySelector('.menu-label');
            return label ? label.textContent : '';
        }
        return '';
    }

    setupEventListeners() {
        // Close submenus when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.menuElement.contains(e.target)) {
                this.closeAllSubmenus();
            }
        });

        // Handle window resize for responsive behavior
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    setupKeyboardNavigation() {
        this.keydownHandler = (e) => {
            this.handleKeydown(e);
        };

        this.menuElement.addEventListener('keydown', this.keydownHandler);

        // Set up initial focus
        this.setupInitialFocus();
    }

    setupInitialFocus() {
        const firstItem = this.menuElement.querySelector('.menu-link, .menu-submenu-toggle');
        if (firstItem) {
            firstItem.setAttribute('tabindex', '0');
            this.focusedItem = firstItem;
        }
    }

    handleKeydown(e) {
        const focusableItems = Array.from(
            this.menuElement.querySelectorAll('.menu-link:not([disabled]), .menu-submenu-toggle:not([disabled])')
        );

        const currentIndex = focusableItems.indexOf(this.focusedItem);
        let newIndex = currentIndex;

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                newIndex = currentIndex < focusableItems.length - 1 ? currentIndex + 1 : 0;
                break;

            case 'ArrowUp':
                e.preventDefault();
                newIndex = currentIndex > 0 ? currentIndex - 1 : focusableItems.length - 1;
                break;

            case 'ArrowRight':
                e.preventDefault();
                if (this.focusedItem.classList.contains('menu-submenu-toggle')) {
                    this.focusedItem.click();
                }
                break;

            case 'ArrowLeft':
                e.preventDefault();
                if (this.focusedItem.classList.contains('menu-submenu-toggle')) {
                    const key = this.getItemKey(this.focusedItem.parentElement);
                    if (this.openSubmenus.has(key)) {
                        this.closeSubmenu(key, this.focusedItem);
                    }
                }
                break;

            case 'Enter':
            case ' ':
                e.preventDefault();
                this.focusedItem.click();
                break;

            case 'Escape':
                e.preventDefault();
                this.closeAllSubmenus();
                break;
        }

        if (newIndex !== currentIndex) {
            this.moveFocus(focusableItems[newIndex]);
        }
    }

    moveFocus(newFocusItem) {
        if (this.focusedItem) {
            this.focusedItem.setAttribute('tabindex', '-1');
        }

        this.focusedItem = newFocusItem;
        this.focusedItem.setAttribute('tabindex', '0');
        this.focusedItem.focus();
    }

    closeAllSubmenus() {
        const submenuToggleButtons = this.menuElement.querySelectorAll('.menu-submenu-toggle');
        submenuToggleButtons.forEach(button => {
            const key = this.getItemKey(button.parentElement);
            if (this.openSubmenus.has(key)) {
                this.closeSubmenu(key, button);
            }
        });
    }

    handleResize() {
        // Handle responsive behavior if needed
        if (this.props.responsive) {
            const width = window.innerWidth;
            // Add responsive logic here
        }
    }

    callCallback(callback, data) {
        if (typeof callback === 'function') {
            callback(data);
        } else if (typeof callback === 'string') {
            try {
                const func = new Function('data', callback);
                func(data);
            } catch (e) {
                console.error('Error executing callback:', e);
            }
        }
    }

    updateProps(newProps) {
        this.props = { ...this.props, ...newProps };
        this.render();
    }

    collapse() {
        this.props.collapsed = true;
        this.menuElement.classList.add('menu-collapsed');
        this.closeAllSubmenus();
    }

    expand() {
        this.props.collapsed = false;
        this.menuElement.classList.remove('menu-collapsed');
    }

    destroy() {
        if (this.keydownHandler) {
            this.menuElement.removeEventListener('keydown', this.keydownHandler);
        }

        // Clean up event listeners
        window.removeEventListener('resize', this.handleResize);
    }
}

// Export for use in other components
window.MenuRenderer = MenuRenderer;;

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['menu'] = menuRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: menu', error);
    }
})();

// Auto-generated component: navbar
(function(){
    try {
        const navbarRenderer = /**
 * Navbar Component JavaScript
 * Handles rendering and interaction for navbar elements
 */

class NavbarRenderer {
    constructor(containerId, props = {}) {
        this.containerId = containerId;
        this.props = props;
        this.navbarElement = null;
        this.isCollapsed = false;
        this.mobileBreakpoint = 768;
        this.scrollThreshold = 100;
        this.lastScrollY = 0;
        this.isScrolled = false;
        this.resizeObserver = null;
        this.scrollTimeout = null;
        
        this.init();
    }

    init() {
        this.render();
        this.setupEventListeners();
        this.handleResponsive();
        this.handleScroll();
    }

    render() {
        const container = document.getElementById(this.containerId);
        if (!container) return;

        const navbar = this.createNavbar();
        container.innerHTML = '';
        container.appendChild(navbar);
        
        this.navbarElement = navbar;
    }

    createNavbar() {
        const navbar = document.createElement('nav');
        navbar.className = this.getNavbarClasses();
        navbar.setAttribute('role', 'navigation');
        navbar.setAttribute('aria-label', this.props.ariaLabel || 'Main navigation');

        // Create navbar container
        const navContainer = document.createElement('div');
        navContainer.className = 'navbar-container';

        // Create brand section
        if (this.props.brand) {
            const brandElement = this.createBrand();
            navContainer.appendChild(brandElement);
        }

        // Create toggle button for mobile
        const toggleButton = this.createToggleButton();
        navContainer.appendChild(toggleButton);

        // Create navigation items container
        const navItems = this.createNavItems();
        navContainer.appendChild(navItems);

        // Create actions section
        if (this.props.actions && this.props.actions.length > 0) {
            const actionsElement = this.createActions();
            navContainer.appendChild(actionsElement);
        }

        navbar.appendChild(navContainer);
        return navbar;
    }

    createBrand() {
        const brand = document.createElement('div');
        brand.className = 'navbar-brand';

        if (this.props.brand.logo) {
            const logo = document.createElement('img');
            logo.src = this.props.brand.logo;
            logo.alt = this.props.brand.alt || 'Logo';
            logo.className = 'navbar-logo';
            brand.appendChild(logo);
        }

        if (this.props.brand.text) {
            const text = document.createElement('span');
            text.textContent = this.props.brand.text;
            text.className = 'navbar-brand-text';
            brand.appendChild(text);
        }

        if (this.props.brand.url) {
            const link = document.createElement('a');
            link.href = this.props.brand.url;
            link.className = 'navbar-brand-link';
            link.appendChild(brand.cloneNode(true));
            brand.innerHTML = '';
            brand.appendChild(link);
        }

        return brand;
    }

    createToggleButton() {
        const button = document.createElement('button');
        button.className = 'navbar-toggle';
        button.setAttribute('type', 'button');
        button.setAttribute('aria-label', 'Toggle navigation');
        button.setAttribute('aria-expanded', 'false');
        button.setAttribute('aria-controls', 'navbar-collapse');

        // Create hamburger icon
        const icon = document.createElement('span');
        icon.className = 'navbar-toggle-icon';
        icon.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;

        button.appendChild(icon);

        button.addEventListener('click', () => {
            this.toggleNavbar();
        });

        return button;
    }

    createNavItems() {
        const navCollapse = document.createElement('div');
        navCollapse.className = 'navbar-collapse';
        navCollapse.id = 'navbar-collapse';

        const navList = document.createElement('ul');
        navList.className = 'navbar-nav';

        if (this.props.items && this.props.items.length > 0) {
            this.props.items.forEach(item => {
                const listItem = this.createNavItem(item);
                navList.appendChild(listItem);
            });
        }

        navCollapse.appendChild(navList);
        return navCollapse;
    }

    createNavItem(item) {
        const listItem = document.createElement('li');
        listItem.className = 'navbar-nav-item';

        if (item.dropdown && item.dropdown.length > 0) {
            // Create dropdown
            listItem.className += ' navbar-dropdown';
            const dropdownToggle = this.createDropdownToggle(item);
            const dropdownMenu = this.createDropdownMenu(item.dropdown);
            
            listItem.appendChild(dropdownToggle);
            listItem.appendChild(dropdownMenu);
        } else {
            // Create regular nav item
            const link = document.createElement('a');
            link.href = item.url || '#';
            link.className = 'navbar-nav-link';
            link.textContent = item.text;

            if (item.active) {
                link.className += ' navbar-nav-active';
            }

            if (item.disabled) {
                link.className += ' navbar-nav-disabled';
                link.setAttribute('aria-disabled', 'true');
            }

            if (item.icon) {
                const icon = document.createElement('i');
                icon.className = `navbar-nav-icon ${item.icon}`;
                link.insertBefore(icon, link.firstChild);
            }

            listItem.appendChild(link);
        }

        return listItem;
    }

    createDropdownToggle(item) {
        const toggle = document.createElement('button');
        toggle.className = 'navbar-dropdown-toggle';
        toggle.textContent = item.text;
        toggle.setAttribute('aria-haspopup', 'true');
        toggle.setAttribute('aria-expanded', 'false');

        if (item.icon) {
            const icon = document.createElement('i');
            icon.className = `navbar-nav-icon ${item.icon}`;
            toggle.insertBefore(icon, toggle.firstChild);
        }

        const caret = document.createElement('i');
        caret.className = 'navbar-dropdown-caret';
        toggle.appendChild(caret);

        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleDropdown(toggle);
        });

        return toggle;
    }

    createDropdownMenu(items) {
        const menu = document.createElement('ul');
        menu.className = 'navbar-dropdown-menu';
        menu.setAttribute('role', 'menu');

        items.forEach(item => {
            const listItem = document.createElement('li');
            listItem.className = 'navbar-dropdown-item';

            if (item.divider) {
                listItem.className += ' navbar-dropdown-divider';
            } else {
                const link = document.createElement('a');
                link.href = item.url || '#';
                link.className = 'navbar-dropdown-link';
                link.textContent = item.text;
                link.setAttribute('role', 'menuitem');

                if (item.icon) {
                    const icon = document.createElement('i');
                    icon.className = `navbar-dropdown-icon ${item.icon}`;
                    link.insertBefore(icon, link.firstChild);
                }

                listItem.appendChild(link);
            }

            menu.appendChild(listItem);
        });

        return menu;
    }

    createActions() {
        const actions = document.createElement('div');
        actions.className = 'navbar-actions';

        this.props.actions.forEach(action => {
            const button = document.createElement('button');
            button.className = `navbar-action ${action.variant || 'default'}`;
            button.textContent = action.text;

            if (action.icon) {
                const icon = document.createElement('i');
                icon.className = `navbar-action-icon ${action.icon}`;
                button.insertBefore(icon, button.firstChild);
            }

            if (action.onClick) {
                button.addEventListener('click', action.onClick);
            }

            actions.appendChild(button);
        });

        return actions;
    }

    getNavbarClasses() {
        let classes = 'navbar';

        if (this.props.variant) {
            classes += ` navbar-${this.props.variant}`;
        }

        if (this.props.position) {
            classes += ` navbar-${this.props.position}`;
        }

        if (this.props.transparent) {
            classes += ' navbar-transparent';
        }

        if (this.props.shadow) {
            classes += ' navbar-shadow';
        }

        if (this.props.sticky) {
            classes += ' navbar-sticky';
        }

        if (this.isScrolled) {
            classes += ' navbar-scrolled';
        }

        if (this.isCollapsed) {
            classes += ' navbar-collapsed';
        }

        return classes;
    }

    toggleNavbar() {
        this.isCollapsed = !this.isCollapsed;
        const toggle = this.navbarElement.querySelector('.navbar-toggle');
        const collapse = this.navbarElement.querySelector('.navbar-collapse');

        if (this.isCollapsed) {
            this.navbarElement.classList.add('navbar-collapsed');
            toggle.setAttribute('aria-expanded', 'true');
            collapse.style.maxHeight = collapse.scrollHeight + 'px';
        } else {
            this.navbarElement.classList.remove('navbar-collapsed');
            toggle.setAttribute('aria-expanded', 'false');
            collapse.style.maxHeight = '0';
        }
    }

    toggleDropdown(toggle) {
        const menu = toggle.nextElementSibling;
        const isExpanded = toggle.getAttribute('aria-expanded') === 'true';

        // Close all other dropdowns
        const allDropdowns = this.navbarElement.querySelectorAll('.navbar-dropdown-toggle');
        allDropdowns.forEach(dropdown => {
            if (dropdown !== toggle) {
                dropdown.setAttribute('aria-expanded', 'false');
                dropdown.parentElement.classList.remove('navbar-dropdown-open');
            }
        });

        // Toggle current dropdown
        toggle.setAttribute('aria-expanded', !isExpanded);
        toggle.parentElement.classList.toggle('navbar-dropdown-open');
    }

    handleResponsive() {
        const checkWidth = () => {
            const width = window.innerWidth;
            if (width >= this.mobileBreakpoint) {
                this.isCollapsed = false;
                this.navbarElement.classList.remove('navbar-collapsed');
                const collapse = this.navbarElement.querySelector('.navbar-collapse');
                collapse.style.maxHeight = '';
            }
        };

        window.addEventListener('resize', checkWidth);
        checkWidth();
    }

    handleScroll() {
        if (!this.props.sticky) return;

        const handleScrollEvent = () => {
            const currentScrollY = window.scrollY;
            const scrolledPastThreshold = currentScrollY > this.scrollThreshold;

            if (scrolledPastThreshold !== this.isScrolled) {
                this.isScrolled = scrolledPastThreshold;
                this.updateScrollClasses();
            }

            this.lastScrollY = currentScrollY;
        };

        window.addEventListener('scroll', handleScrollEvent);
        handleScrollEvent();
    }

    updateScrollClasses() {
        if (this.isScrolled) {
            this.navbarElement.classList.add('navbar-scrolled');
        } else {
            this.navbarElement.classList.remove('navbar-scrolled');
        }
    }

    setupEventListeners() {
        // Close dropdowns when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.navbar-dropdown')) {
                const dropdowns = this.navbarElement.querySelectorAll('.navbar-dropdown-toggle');
                dropdowns.forEach(dropdown => {
                    dropdown.setAttribute('aria-expanded', 'false');
                    dropdown.parentElement.classList.remove('navbar-dropdown-open');
                });
            }
        });

        // Handle keyboard navigation
        this.navbarElement.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                // Close all dropdowns
                const dropdowns = this.navbarElement.querySelectorAll('.navbar-dropdown-toggle');
                dropdowns.forEach(dropdown => {
                    dropdown.setAttribute('aria-expanded', 'false');
                    dropdown.parentElement.classList.remove('navbar-dropdown-open');
                });
            }
        });
    }

    updateProps(newProps) {
        this.props = { ...this.props, ...newProps };
        this.render();
    }

    destroy() {
        if (this.resizeObserver) {
            this.resizeObserver.disconnect();
        }
        
        if (this.scrollTimeout) {
            clearTimeout(this.scrollTimeout);
        }
        
        // Remove event listeners
        window.removeEventListener('resize', this.handleResponsive);
        window.removeEventListener('scroll', this.handleScroll);
    }
}

// Export for use in other components
window.NavbarRenderer = NavbarRenderer;;

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['navbar'] = navbarRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: navbar', error);
    }
})();

// Auto-generated component: nav_item
(function(){
    try {
        const nav_itemRenderer = // Sidebar component renderer
(component) => {
    const el = document.createElement("div");
    el.className = "nav-item";
    
    // If children array is available, use that
    if (component.props?.children && Array.isArray(component.props.children)) {
        component.props.children.forEach(child => {
            el.appendChild(window.CacaoCore.renderComponent(child));
        });
    } else {
        // Simple/legacy rendering
        if (component.props?.icon) {
            const iconSpan = document.createElement("span");
            window.CacaoCore.applyContent(iconSpan, component.props.icon);
            iconSpan.style.marginRight = "8px";
            el.appendChild(iconSpan);
        }
        if (component.props?.label) {
            const labelSpan = document.createElement("span");
            window.CacaoCore.applyContent(labelSpan, component.props.label);
            el.appendChild(labelSpan);
        }
    }
    
    if (component.props?.isActive) {
        el.classList.add("active");
    }
    
    if (component.props?.onClick) {
        el.onclick = async () => {
            try {
                const action = component.props.onClick.action;
                const state = component.props.onClick.state;
                const value = component.props.onClick.value;
                const immediate = component.props.onClick.immediate === true;
                
                // Check if we're clicking the same page
                if (state === 'current_page' && window.location.hash === `#${value}`) {
                    console.log("[CacaoCore] Clicked same page, skipping refresh");
                    return;
                }
                
                document.querySelector('.refresh-overlay').classList.add('active');
                
                console.log(`[CacaoCore] Handling nav click: ${action} state=${state} value=${value} immediate=${immediate}`);
                
                const response = await fetch(`/api/action?action=${action}&component_type=${state}&value=${value}&immediate=${immediate}&t=${Date.now()}`, {
                    method: 'GET',
                    headers: {
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                        'Expires': '0'
                    }
                });
                
                if (!response.ok) {
                    throw new Error(`Server returned ${response.status}`);
                }
                const data = await response.json();
                console.log("[CacaoCore] Navigation state updated:", data);
                
                if (state === 'current_page') {
                    window.location.hash = value;
                }
                
                if (data.immediate === true) {
                    // fetch UI directly
                    const uiResponse = await fetch(`/api/ui?force=true&_hash=${value}&t=${Date.now()}`, {
                        headers: {
                            'Cache-Control': 'no-cache, no-store, must-revalidate',
                            'Pragma': 'no-cache',
                            'Expires': '0'
                        }
                    });
                    
                    if (!uiResponse.ok) {
                        throw new Error(`UI update failed with status ${uiResponse.status}`);
                    }
                    
                    const uiData = await uiResponse.json();
                    window.CacaoCore.render(uiData);
                } else {
                    // Force UI refresh
                    window.CacaoWS.requestServerRefresh();
                }
            } catch (err) {
                console.error('[CacaoCore] Error handling nav item click:', err);
                document.querySelector('.refresh-overlay').classList.remove('active');
            }
        };
    }
    
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['nav_item'] = nav_itemRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: nav_item', error);
    }
})();

// Auto-generated component: tabs
(function(){
    try {
        const tabsRenderer = /**
 * Tabs Component JavaScript
 * Handles tab switching, animations, and user interactions
 */

class TabsRenderer {
    constructor(containerId, props = {}) {
        this.containerId = containerId;
        this.props = props;
        this.tabsElement = null;
        this.activeKey = props.active_key || null;
        this.animationDuration = 300;
        this.resizeObserver = null;
        this.keyboardHandlers = new Map();
        
        this.init();
    }

    init() {
        this.render();
        this.setupEventListeners();
        this.setupKeyboardNavigation();
        this.setupResizeObserver();
    }

    render() {
        const container = document.getElementById(this.containerId);
        if (!container) return;

        const tabsContainer = this.createTabsContainer();
        container.innerHTML = '';
        container.appendChild(tabsContainer);
        
        this.tabsElement = tabsContainer;
        this.updateActiveIndicator();
    }

    createTabsContainer() {
        const container = document.createElement('div');
        container.className = this.getContainerClasses();
        container.setAttribute('role', 'tablist');
        container.setAttribute('aria-orientation', this.props.orientation || 'horizontal');

        if (this.props.max_width) {
            container.style.maxWidth = this.props.max_width;
        }

        // Create tab navigation
        const tabNav = this.createTabNavigation();
        container.appendChild(tabNav);

        // Create tab content panels
        const tabContent = this.createTabContent();
        container.appendChild(tabContent);

        return container;
    }

    createTabNavigation() {
        const nav = document.createElement('div');
        nav.className = 'tabs-nav';

        const tabList = document.createElement('div');
        tabList.className = 'tabs-list';

        if (this.props.items && this.props.items.length > 0) {
            this.props.items.forEach(item => {
                const tab = this.createTabItem(item);
                tabList.appendChild(tab);
            });
        }

        // Add button for adding new tabs
        if (this.props.show_add_button) {
            const addButton = this.createAddButton();
            tabList.appendChild(addButton);
        }

        nav.appendChild(tabList);

        // Add active indicator for underline variant
        if (this.props.variant === 'underline') {
            const indicator = document.createElement('div');
            indicator.className = 'tabs-indicator';
            nav.appendChild(indicator);
        }

        return nav;
    }

    createTabItem(item) {
        const tab = document.createElement('button');
        tab.className = this.getTabClasses(item);
        tab.setAttribute('role', 'tab');
        tab.setAttribute('aria-selected', item.key === this.activeKey ? 'true' : 'false');
        tab.setAttribute('aria-controls', `${this.containerId}-panel-${item.key}`);
        tab.setAttribute('id', `${this.containerId}-tab-${item.key}`);
        tab.setAttribute('type', 'button');
        tab.setAttribute('data-key', item.key);

        if (item.disabled) {
            tab.setAttribute('disabled', 'true');
            tab.setAttribute('aria-disabled', 'true');
        }

        // Create tab content
        const tabContent = document.createElement('div');
        tabContent.className = 'tab-content';

        // Add icon if present
        if (item.icon) {
            const icon = document.createElement('i');
            icon.className = `tab-icon ${item.icon}`;
            tabContent.appendChild(icon);
        }

        // Add label
        const label = document.createElement('span');
        label.className = 'tab-label';
        label.textContent = item.label;
        tabContent.appendChild(label);

        // Add badge if present
        if (item.badge !== undefined && item.badge !== null) {
            const badge = document.createElement('span');
            badge.className = 'tab-badge';
            badge.textContent = item.badge;
            tabContent.appendChild(badge);
        }

        // Add close button if closable
        if (this.props.closable || item.closable) {
            const closeButton = document.createElement('button');
            closeButton.className = 'tab-close';
            closeButton.setAttribute('type', 'button');
            closeButton.setAttribute('aria-label', `Close ${item.label}`);
            closeButton.innerHTML = '×';
            
            closeButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.closeTab(item.key);
            });
            
            tabContent.appendChild(closeButton);
        }

        tab.appendChild(tabContent);

        // Add click handler
        tab.addEventListener('click', () => {
            if (!item.disabled) {
                this.setActiveTab(item.key);
            }
        });

        return tab;
    }

    createAddButton() {
        const button = document.createElement('button');
        button.className = 'tabs-add-button';
        button.setAttribute('type', 'button');
        button.setAttribute('aria-label', 'Add new tab');
        button.innerHTML = '<i class="tabs-add-icon">+</i>';

        button.addEventListener('click', () => {
            this.addNewTab();
        });

        return button;
    }

    createTabContent() {
        const content = document.createElement('div');
        content.className = 'tabs-content';

        if (this.props.items && this.props.items.length > 0) {
            this.props.items.forEach(item => {
                const panel = this.createTabPanel(item);
                content.appendChild(panel);
            });
        }

        return content;
    }

    createTabPanel(item) {
        const panel = document.createElement('div');
        panel.className = this.getPanelClasses(item);
        panel.setAttribute('role', 'tabpanel');
        panel.setAttribute('aria-labelledby', `${this.containerId}-tab-${item.key}`);
        panel.setAttribute('id', `${this.containerId}-panel-${item.key}`);
        panel.setAttribute('data-key', item.key);

        if (item.key !== this.activeKey) {
            panel.setAttribute('hidden', 'true');
        }

        // Add content
        if (item.content) {
            if (typeof item.content === 'string') {
                panel.innerHTML = item.content;
            } else if (item.content instanceof HTMLElement) {
                panel.appendChild(item.content);
            }
        }

        return panel;
    }

    getContainerClasses() {
        let classes = 'tabs-container';

        if (this.props.orientation) {
            classes += ` tabs-${this.props.orientation}`;
        }

        if (this.props.size) {
            classes += ` tabs-${this.props.size}`;
        }

        if (this.props.variant) {
            classes += ` tabs-${this.props.variant}`;
        }

        if (this.props.animated) {
            classes += ' tabs-animated';
        }

        if (this.props.closable) {
            classes += ' tabs-closable';
        }

        if (this.props.centered) {
            classes += ' tabs-centered';
        }

        if (this.props.show_add_button) {
            classes += ' tabs-has-add-button';
        }

        return classes;
    }

    getTabClasses(item) {
        let classes = 'tab-item';

        if (item.key === this.activeKey) {
            classes += ' tab-active';
        }

        if (item.disabled) {
            classes += ' tab-disabled';
        }

        if (this.props.closable || item.closable) {
            classes += ' tab-closable';
        }

        return classes;
    }

    getPanelClasses(item) {
        let classes = 'tab-panel';

        if (item.key === this.activeKey) {
            classes += ' tab-panel-active';
        }

        return classes;
    }

    setActiveTab(key) {
        if (this.activeKey === key) return;

        const oldKey = this.activeKey;
        this.activeKey = key;

        // Update tab buttons
        const tabs = this.tabsElement.querySelectorAll('.tab-item');
        tabs.forEach(tab => {
            const tabKey = tab.getAttribute('data-key');
            const isActive = tabKey === key;
            
            tab.classList.toggle('tab-active', isActive);
            tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
        });

        // Update panels
        this.updatePanels(oldKey, key);

        // Update active indicator
        this.updateActiveIndicator();

        // Call change callback
        if (this.props.on_change) {
            this.callCallback(this.props.on_change, { key, oldKey });
        }
    }

    updatePanels(oldKey, newKey) {
        const panels = this.tabsElement.querySelectorAll('.tab-panel');
        
        panels.forEach(panel => {
            const panelKey = panel.getAttribute('data-key');
            const isActive = panelKey === newKey;
            
            panel.classList.toggle('tab-panel-active', isActive);
            
            if (this.props.animated) {
                if (isActive) {
                    panel.removeAttribute('hidden');
                    panel.style.opacity = '0';
                    panel.style.transform = 'translateX(10px)';
                    
                    requestAnimationFrame(() => {
                        panel.style.transition = `opacity ${this.animationDuration}ms ease, transform ${this.animationDuration}ms ease`;
                        panel.style.opacity = '1';
                        panel.style.transform = 'translateX(0)';
                    });
                } else {
                    panel.style.transition = `opacity ${this.animationDuration}ms ease`;
                    panel.style.opacity = '0';
                    
                    setTimeout(() => {
                        panel.setAttribute('hidden', 'true');
                        panel.style.transition = '';
                        panel.style.transform = '';
                    }, this.animationDuration);
                }
            } else {
                if (isActive) {
                    panel.removeAttribute('hidden');
                } else {
                    panel.setAttribute('hidden', 'true');
                }
            }
        });
    }

    updateActiveIndicator() {
        const indicator = this.tabsElement.querySelector('.tabs-indicator');
        if (!indicator) return;

        const activeTab = this.tabsElement.querySelector('.tab-active');
        if (!activeTab) return;

        const tabList = this.tabsElement.querySelector('.tabs-list');
        const tabRect = activeTab.getBoundingClientRect();
        const listRect = tabList.getBoundingClientRect();

        if (this.props.orientation === 'vertical') {
            indicator.style.top = `${activeTab.offsetTop}px`;
            indicator.style.height = `${activeTab.offsetHeight}px`;
            indicator.style.width = '3px';
            indicator.style.left = '0';
        } else {
            indicator.style.left = `${activeTab.offsetLeft}px`;
            indicator.style.width = `${activeTab.offsetWidth}px`;
            indicator.style.height = '3px';
            indicator.style.top = 'auto';
        }
    }

    closeTab(key) {
        if (this.props.items.length <= 1) return; // Don't close if it's the last tab

        // Find the tab to close
        const tabIndex = this.props.items.findIndex(item => item.key === key);
        if (tabIndex === -1) return;

        // Remove from items array
        this.props.items.splice(tabIndex, 1);

        // Update active key if needed
        if (this.activeKey === key) {
            const newActiveIndex = Math.min(tabIndex, this.props.items.length - 1);
            this.activeKey = this.props.items[newActiveIndex]?.key || null;
        }

        // Re-render
        this.render();

        // Call close callback
        if (this.props.on_close) {
            this.callCallback(this.props.on_close, { key });
        }
    }

    addNewTab() {
        if (this.props.on_add) {
            this.callCallback(this.props.on_add, {});
        }
    }

    setupEventListeners() {
        // Handle window resize for indicator positioning
        window.addEventListener('resize', () => {
            this.updateActiveIndicator();
        });

        // Handle tab switching with mouse wheel (on tab navigation)
        const tabNav = this.tabsElement.querySelector('.tabs-nav');
        if (tabNav) {
            tabNav.addEventListener('wheel', (e) => {
                if (e.deltaY !== 0) {
                    e.preventDefault();
                    this.navigateWithWheel(e.deltaY > 0 ? 1 : -1);
                }
            });
        }
    }

    setupKeyboardNavigation() {
        this.tabsElement.addEventListener('keydown', (e) => {
            const tabs = Array.from(this.tabsElement.querySelectorAll('.tab-item:not(.tab-disabled)'));
            const currentIndex = tabs.findIndex(tab => tab.getAttribute('data-key') === this.activeKey);
            
            let newIndex = currentIndex;
            
            switch (e.key) {
                case 'ArrowLeft':
                case 'ArrowUp':
                    e.preventDefault();
                    newIndex = currentIndex > 0 ? currentIndex - 1 : tabs.length - 1;
                    break;
                    
                case 'ArrowRight':
                case 'ArrowDown':
                    e.preventDefault();
                    newIndex = currentIndex < tabs.length - 1 ? currentIndex + 1 : 0;
                    break;
                    
                case 'Home':
                    e.preventDefault();
                    newIndex = 0;
                    break;
                    
                case 'End':
                    e.preventDefault();
                    newIndex = tabs.length - 1;
                    break;
                    
                case 'Enter':
                case ' ':
                    e.preventDefault();
                    if (tabs[currentIndex]) {
                        tabs[currentIndex].click();
                    }
                    break;
            }
            
            if (newIndex !== currentIndex && tabs[newIndex]) {
                const newKey = tabs[newIndex].getAttribute('data-key');
                this.setActiveTab(newKey);
                tabs[newIndex].focus();
            }
        });
    }

    setupResizeObserver() {
        if (!window.ResizeObserver) return;

        this.resizeObserver = new ResizeObserver(() => {
            this.updateActiveIndicator();
        });

        this.resizeObserver.observe(this.tabsElement);
    }

    navigateWithWheel(direction) {
        const enabledItems = this.props.items.filter(item => !item.disabled);
        const currentIndex = enabledItems.findIndex(item => item.key === this.activeKey);
        
        if (currentIndex === -1) return;
        
        let newIndex;
        if (direction > 0) {
            newIndex = currentIndex < enabledItems.length - 1 ? currentIndex + 1 : 0;
        } else {
            newIndex = currentIndex > 0 ? currentIndex - 1 : enabledItems.length - 1;
        }
        
        this.setActiveTab(enabledItems[newIndex].key);
    }

    callCallback(callback, data) {
        if (typeof callback === 'function') {
            callback(data);
        } else if (typeof callback === 'string') {
            // Try to evaluate as a function
            try {
                const func = new Function('data', callback);
                func(data);
            } catch (e) {
                console.error('Error executing callback:', e);
            }
        }
    }

    updateProps(newProps) {
        this.props = { ...this.props, ...newProps };
        
        if (newProps.active_key !== undefined) {
            this.activeKey = newProps.active_key;
        }
        
        this.render();
    }

    getActiveKey() {
        return this.activeKey;
    }

    getActiveItem() {
        return this.props.items.find(item => item.key === this.activeKey) || null;
    }

    destroy() {
        if (this.resizeObserver) {
            this.resizeObserver.disconnect();
        }
        
        // Clean up event listeners
        this.keyboardHandlers.clear();
        
        // Remove window resize listener
        window.removeEventListener('resize', this.updateActiveIndicator);
    }
}

// Export for use in other components
window.TabsRenderer = TabsRenderer;;

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['tabs'] = tabsRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: tabs', error);
    }
})();

// Auto-generated component: button
(function(){
    try {
        const buttonRenderer = // Button Component Renderer
(component) => {
    const el = document.createElement("button");
    el.className = "button";
    window.CacaoCore.applyContent(el, component.props.label);
    
    if (component.props?.action) {
        el.onclick = async () => {
            try {
                console.log("[Cacao] Sending event:", component.props.on_click || component.props.action);
                document.querySelector('.refresh-overlay').classList.add('active');
                
                const parentSection = el.closest('section[data-component-type]');
                const componentType = parentSection ? parentSection.dataset.componentType : 'unknown';
                
                // If WebSocket is open
                if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
                    const eventName = component.props.on_click || component.props.action;
                    console.log("[Cacao] Sending WebSocket event:", eventName);
                    // Include the data property from the component if available
                    const eventData = { component_type: componentType };
                    
                    // Add the data property from the component if it exists
                    if (component.props.data) {
                        console.log("[Cacao] Including custom data in event:", component.props.data);
                        Object.assign(eventData, component.props.data);
                    }
                    
                    window.socket.send(JSON.stringify({
                        type: 'event',
                        event: eventName,
                        data: eventData
                    }));
                } else {
                    // Fallback to HTTP
                    console.log("[Cacao] WebSocket not available, using HTTP fallback");
                    const action = component.props.on_click || component.props.action;
                    // Build query parameters including custom data
                    let queryParams = `action=${action}&component_type=${componentType}`;
                    
                    // Add the data property from the component if it exists
                    if (component.props.data) {
                        console.log("[Cacao] Including custom data in HTTP fallback:", component.props.data);
                        for (const [key, value] of Object.entries(component.props.data)) {
                            queryParams += `&${key}=${encodeURIComponent(value)}`;
                        }
                    }
                    
                    const response = await fetch(`/api/action?${queryParams}&t=${Date.now()}`, {
                        method: 'GET',
                        headers: {
                            'Cache-Control': 'no-cache, no-store, must-revalidate',
                            'Pragma': 'no-cache',
                            'Expires': '0'
                        }
                    });
                    
                    if (!response.ok) {
                        const errorText = await response.text();
                        console.error("[Cacao] Server error response:", errorText);
                        throw new Error(`Server returned ${response.status}: ${errorText}`);
                    }
                    
                    const responseData = await response.json();
                    console.log("[CacaoCore] Server response data:", responseData);
                    window.CacaoWS.requestServerRefresh();
                }
            } catch (err) {
                console.error('Error handling action:', err);
                document.querySelector('.refresh-overlay').classList.remove('active');
                
                if (errorCount < MAX_ERROR_ALERTS) {
                    errorCount++;
                    alert(`Error: ${err.message}\nPlease try again or reload the page.`);
                } else if (errorCount === MAX_ERROR_ALERTS) {
                    errorCount++;
                    console.error("Too many errors. Suppressing further alerts.");
                }
            }
        };
    }
    
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['button'] = buttonRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: button', error);
    }
})();

// Auto-generated component: sidebar
(function(){
    try {
        const sidebarRenderer = // Sidebar component renderer
(component) => {
    const el = document.createElement("div");
    el.className = "sidebar";
    
    // Apply styles from props
    if (component.props?.style) {
        Object.assign(el.style, component.props.style);
    }
    if (component.props?.content) {
        window.CacaoCore.applyContent(el, component.props.content);
    }
    if (component.children) {
        window.CacaoCore.renderChildren(el, component.children);
    } else if (component.props?.children) {
        window.CacaoCore.renderChildren(el, component.props.children);
    }
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['sidebar'] = sidebarRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: sidebar', error);
    }
})();

// Auto-generated component: text
(function(){
    try {
        const textRenderer = // Text component renderer
(component) => {
    const el = document.createElement("p");
    el.className = "text";
    window.CacaoCore.applyContent(el, component.props.content);
    return el;
};

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['text'] = textRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: text', error);
    }
})();
