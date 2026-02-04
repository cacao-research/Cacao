/*
 * Auto-generated Cacao Components
 * Generated on: 2025-07-21 19:10:24
 * Components: 37
 *
 * This file extends window.CacaoCore.componentRenderers with compiled components.
 * It must be loaded AFTER cacao-core.js to ensure the global registry exists.
 */


// Auto-generated component: _template
(function(){
    try {
        // Helper functions and global definitions
        // Template for creating new Cacao components
// Copy this file to your component directory and modify as needed

// Component renderer function
        
        // Main component renderer
        const _templateRenderer = (component) => {
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        // Merged Table Component JavaScript Renderer for Cacao Framework
// Supports both simple native rendering and advanced DataTables.js functionality

// === Global Filter Panel Functions ===
// These functions must be globally available for onclick handlers

window.closeFilterPanel = function(tableId) {
    const panel = document.getElementById(`filter-panel-${tableId}`);
    const overlay = document.getElementById(`filter-overlay-${tableId}`);
    if (panel && overlay) {
        closeFilterPanel(panel, overlay);
    }
};

// Global filter state storage
window.cacaoTableFilters = window.cacaoTableFilters || {};

window.applyAdvancedFilters = function(tableId) {
    console.log('[DEBUG] ==> applyAdvancedFilters called for tableId:', tableId);
    
    const table = document.getElementById(tableId);
    const wrapper = table ? table.closest('.datatable-wrapper') : null;
    
    console.log('[DEBUG] DOM elements found:', {
        table: !!table,
        wrapper: !!wrapper,
        dataTable: wrapper ? !!wrapper._dataTable : false
    });
    
    if (!table || !wrapper || !wrapper._dataTable) {
        console.error('[DEBUG] EARLY EXIT: DataTable not found for advanced filters');
        console.log('[DEBUG] Available table IDs:', Array.from(document.querySelectorAll('table')).map(t => t.id));
        return;
    }
    
    const dataTable = window.jQuery(`#${tableId}`).DataTable();
    const panel = document.getElementById(`filter-panel-${tableId}`);
    const toggleBtn = wrapper._filterToggle;
    
    console.log('[DEBUG] DataTable instance obtained:', !!dataTable);
    console.log('[DEBUG] Filter panel found:', !!panel);
    
    if (!panel) {
        console.error('[DEBUG] EARLY EXIT: Filter panel not found! Expected ID:', `filter-panel-${tableId}`);
        console.log('[DEBUG] Available filter panels:', Array.from(document.querySelectorAll('[id*="filter-panel"]')).map(p => p.id));
        return;
    }
    
    // Collect filter values with enhanced debugging
    const filters = {};
    const filterInputs = panel.querySelectorAll('[id^="filter-"]');
    let hasActiveFilters = false;
    
    console.log('[DEBUG] Found filter inputs:', filterInputs.length);
    console.log('[DEBUG] Filter input IDs:', Array.from(filterInputs).map(input => ({id: input.id, value: input.value, type: input.type})));
    
    filterInputs.forEach(input => {
        console.log('[DEBUG] Processing filter input:', input.id, 'value:', input.value);
        const idParts = input.id.split('-');
        console.log('[DEBUG] ID parts:', idParts);
        
        if (idParts.length >= 4) {
            // Fixed column name extraction - handle split tableId
            // Expected format: filter-table-{randomId}-{columnName}-{fieldType}
            // idParts: ['filter', 'table', 'randomId', 'columnName', 'fieldType']
            
            if (idParts[0] !== 'filter' || idParts[1] !== 'table') {
                console.warn('[DEBUG] Unexpected ID format:', input.id);
                return;
            }
            
            // Extract parts after 'table-randomId'
            const columnParts = idParts.slice(3, -1); // Skip 'filter', 'table', 'randomId' and fieldType
            const columnName = columnParts.join('-');
            const fieldType = idParts[idParts.length - 1];
            
            console.log('[DEBUG] Extracted:', {columnName, fieldType, idParts});
            
            if (fieldType === 'type') {
                // Skip type selectors
                return;
            }
            
            if (fieldType === 'min' || fieldType === 'max') {
                // Range filter
                console.log('[DEBUG] Range filter processing:', {columnName, fieldType, value: input.value});
                
                if (input.value && input.value.trim() !== '') {
                    if (!filters[columnName]) {
                        filters[columnName] = { type: 'range' };
                    }
                    filters[columnName][fieldType] = input.value.trim();
                    hasActiveFilters = true;
                    console.log('[DEBUG] ✅ Added range filter:', columnName, filters[columnName]);
                } else {
                    console.log('[DEBUG] ❌ Skipping empty range filter:', columnName, fieldType);
                }
            } else if (fieldType === 'value') {
                // Regular filter
                const typeSelect = document.getElementById(`filter-${tableId}-${columnName}-type`);
                const filterType = typeSelect ? typeSelect.value : 'contains';
                
                console.log('[DEBUG] Regular filter processing:');
                console.log('[DEBUG] - Column:', columnName);
                console.log('[DEBUG] - Input value:', input.value);
                console.log('[DEBUG] - Filter type:', filterType);
                console.log('[DEBUG] - Type select found:', !!typeSelect);
                
                if (input.value && input.value.trim() !== '') {
                    filters[columnName] = {
                        type: filterType,
                        value: input.value.trim()
                    };
                    hasActiveFilters = true;
                    console.log('[DEBUG] ✅ Added filter for column:', columnName, filters[columnName]);
                } else {
                    console.log('[DEBUG] ❌ Skipping empty filter for column:', columnName);
                }
            }
        }
    });
    
    // Store filters globally for use by DataTable AJAX function
    window.cacaoTableFilters[tableId] = filters;
    
    // Update toggle button state
    if (toggleBtn) {
        if (hasActiveFilters) {
            toggleBtn.classList.add('has-filters');
        } else {
            toggleBtn.classList.remove('has-filters');
        }
    }
    
    console.log('[DEBUG] Applying advanced filters:', filters);
    console.log('[DEBUG] Stored filters globally for table:', tableId);
    console.log('[DEBUG] Has active filters:', hasActiveFilters);
    
    // Trigger DataTable refresh - the AJAX data function will pick up the stored filters
    console.log('[DEBUG] Calling dataTable.draw()');
    dataTable.draw();
    
    // Close filter panel
    window.closeFilterPanel(tableId);
    
    console.log('Applied advanced filters:', filters);
};

window.clearAdvancedFilters = function(tableId) {
    const panel = document.getElementById(`filter-panel-${tableId}`);
    const table = document.getElementById(tableId);
    const wrapper = table ? table.closest('.datatable-wrapper') : null;
    const toggleBtn = wrapper ? wrapper._filterToggle : null;
    
    // Clear all filter inputs
    const filterInputs = panel.querySelectorAll('input, select');
    filterInputs.forEach(input => {
        if (input.type === 'select-one') {
            input.selectedIndex = 0;
        } else {
            input.value = '';
        }
    });
    
    // Update toggle button state
    if (toggleBtn) {
        toggleBtn.classList.remove('has-filters');
    }
    
    // Clear stored filters
    if (window.cacaoTableFilters) {
        window.cacaoTableFilters[tableId] = {};
    }
    
    // Refresh DataTable - the AJAX data function will pick up the cleared filters
    if (table && wrapper && wrapper._dataTable) {
        const dataTable = window.jQuery(`#${tableId}`).DataTable();
        console.log('[DEBUG] Clearing filters and refreshing DataTable');
        dataTable.draw();
    }
    
    console.log('Cleared all advanced filters');
};

// === Helper Functions for Filter Panel ===

function closeFilterPanel(panel, overlay) {
    panel.classList.add("animating-out");
    panel.classList.remove("open");
    overlay.classList.remove("visible");
    
    setTimeout(() => {
        panel.classList.remove("animating-out");
    }, 300);
}

function openFilterPanel(panel, overlay) {
    panel.classList.add("animating-in");
    panel.classList.add("open");
    overlay.classList.add("visible");
    
    setTimeout(() => {
        panel.classList.remove("animating-in");
    }, 300);
}

function createFilterPanel(tableId, props) {
    // Create overlay
    const overlay = document.createElement("div");
    overlay.id = `filter-overlay-${tableId}`;
    overlay.className = "table-filter-panel-overlay";
    overlay.onclick = () => {
        const panel = document.getElementById(`filter-panel-${tableId}`);
        closeFilterPanel(panel, overlay);
    };
    document.body.appendChild(overlay);
    
    // Create filter panel
    const panel = document.createElement("div");
    panel.id = `filter-panel-${tableId}`;
    panel.className = "table-filter-panel";
    
    // Create header
    const header = document.createElement("div");
    header.className = "filter-panel-header";
    header.innerHTML = `
        <h3 class="filter-panel-title">Advanced Filters</h3>
        <button class="filter-panel-close" onclick="window.closeFilterPanel('${tableId}')">&times;</button>
    `;
    
    // Create body
    const body = document.createElement("div");
    body.className = "filter-panel-body";
    
    // Generate filter fields based on columns
    if (props.columns && props.columns.length > 0) {
        props.columns.forEach((column, index) => {
            const fieldGroup = createFilterField(column, index, tableId);
            body.appendChild(fieldGroup);
        });
    }
    
    // Create actions
    const actions = document.createElement("div");
    actions.className = "filter-panel-actions";
    actions.innerHTML = `
        <button class="filter-btn filter-btn-primary" onclick="window.applyAdvancedFilters('${tableId}')">Apply Filters</button>
        <button class="filter-btn filter-btn-clear" onclick="window.clearAdvancedFilters('${tableId}')">Clear All</button>
    `;
    
    panel.appendChild(header);
    panel.appendChild(body);
    panel.appendChild(actions);
    
    return panel;
}

function createFilterField(column, index, tableId) {
    const fieldGroup = document.createElement("div");
    fieldGroup.className = "filter-group";
    
    const label = document.createElement("label");
    label.className = "filter-group-label";
    label.textContent = column.title || column.label || `Column ${index + 1}`;
    
    const fieldContainer = document.createElement("div");
    fieldContainer.className = "filter-field";
    
    // Determine field type based on column data type
    const dataIndex = column.dataIndex || column.key || `col_${index}`;
    const fieldType = getColumnFilterType(column);
    
    if (fieldType === 'range') {
        // Numeric range filter
        const rangeContainer = document.createElement("div");
        rangeContainer.className = "filter-range";
        
        const minInput = document.createElement("input");
        minInput.type = "number";
        minInput.placeholder = "Min value";
        minInput.id = `filter-${tableId}-${dataIndex}-min`;
        
        const separator = document.createElement("span");
        separator.className = "filter-range-separator";
        separator.textContent = "to";
        
        const maxInput = document.createElement("input");
        maxInput.type = "number";
        maxInput.placeholder = "Max value";
        maxInput.id = `filter-${tableId}-${dataIndex}-max`;
        
        rangeContainer.appendChild(minInput);
        rangeContainer.appendChild(separator);
        rangeContainer.appendChild(maxInput);
        fieldContainer.appendChild(rangeContainer);
    } else {
        // Text filter with type selection
        const typeSelect = document.createElement("select");
        typeSelect.id = `filter-${tableId}-${dataIndex}-type`;
        typeSelect.innerHTML = `
            <option value="contains">Contains</option>
            <option value="equals">Equals</option>
            <option value="starts_with">Starts with</option>
            <option value="ends_with">Ends with</option>
            ${fieldType === 'numeric' ? `
                <option value="greater_than">Greater than</option>
                <option value="less_than">Less than</option>
            ` : ''}
        `;
        
        const valueInput = document.createElement("input");
        valueInput.type = fieldType === 'numeric' ? 'number' : 'text';
        valueInput.placeholder = `Filter ${column.title || 'column'}...`;
        valueInput.id = `filter-${tableId}-${dataIndex}-value`;
        valueInput.style.marginTop = "8px";
        
        fieldContainer.appendChild(typeSelect);
        fieldContainer.appendChild(valueInput);
    }
    
    fieldGroup.appendChild(label);
    fieldGroup.appendChild(fieldContainer);
    
    return fieldGroup;
}

function getColumnFilterType(column) {
    // Determine appropriate filter type based on column properties
    if (column.type === 'number' || column.dataType === 'numeric') {
        return 'range';
    }
    if (column.type === 'date' || column.dataType === 'date') {
        return 'date';
    }
    return 'text';
}

window.toggleAdvancedFilters = function(tableId, props) {
    let panel = document.getElementById(`filter-panel-${tableId}`);
    
    if (!panel) {
        panel = createFilterPanel(tableId, props);
        document.body.appendChild(panel);
    }
    
    const overlay = document.getElementById(`filter-overlay-${tableId}`);
    const isOpen = panel.classList.contains("open");
    
    if (isOpen) {
        closeFilterPanel(panel, overlay);
    } else {
        openFilterPanel(panel, overlay);
    }
};
        
        // Main component renderer
        const tableRenderer = (component) => {
    // === Component Renderer ===
    console.log("[CacaoCore] Rendering merged table component:", component);
    
    const props = component.props;
    const isAdvanced = props.advanced === true;
    const tableId = `table-${Math.random().toString(36).substr(2, 9)}`;
    
    // === DataTables.js Asset Loading Functions ===
    
    function loadDataTablesAssets(props) {
        return new Promise(async (resolve) => {
            // Check if DataTables is already loaded
            if (window.jQuery && window.jQuery.fn.DataTable) {
                resolve();
                return;
            }
            
            try {
                // Step 1: Load jQuery first and ensure it's available
                if (!window.jQuery) {
                    await loadScript('https://code.jquery.com/jquery-3.7.0.min.js');
                    // Wait for jQuery to be globally available
                    await waitForjQuery();
                }
                
                // Step 2: Load DataTables CSS (can be parallel with core JS)
                const cssPromises = [];
                if (!document.querySelector('link[href*="datatables"]')) {
                    cssPromises.push(loadCSS(getDataTablesCSS(props.theme)));
                }
                
                // Step 3: Load DataTables core library after jQuery is confirmed available
                await loadScript('https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js');
                
                // Step 4: Load theme-specific assets (depends on core DataTables)
                if (props.theme === 'bootstrap5') {
                    await loadScript('https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js');
                } else if (props.theme === 'bootstrap4') {
                    await loadScript('https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap4.min.js');
                }
                
                // Step 5: Load additional plugins sequentially (each depends on core DataTables)
                if (props.datatables_config && props.datatables_config.responsive) {
                    await loadScript('https://cdn.datatables.net/responsive/2.5.0/js/dataTables.responsive.min.js');
                    cssPromises.push(loadCSS('https://cdn.datatables.net/responsive/2.5.0/css/responsive.dataTables.min.css'));
                }
                
                if (props.datatables_config && props.datatables_config.fixedHeader) {
                    await loadScript('https://cdn.datatables.net/fixedheader/3.4.0/js/dataTables.fixedHeader.min.js');
                    cssPromises.push(loadCSS('https://cdn.datatables.net/fixedheader/3.4.0/css/fixedHeader.dataTables.min.css'));
                }
                
                if (props.datatables_config && props.datatables_config.select) {
                    await loadScript('https://cdn.datatables.net/select/1.7.0/js/dataTables.select.min.js');
                    cssPromises.push(loadCSS('https://cdn.datatables.net/select/1.7.0/css/select.dataTables.min.css'));
                }
                
                if (props.datatables_config && props.datatables_config.buttons) {
                    // Load buttons plugin dependencies sequentially
                    await loadScript('https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js');
                    
                    // Load button feature dependencies (can be parallel as they don't depend on each other)
                    await Promise.all([
                        loadScript('https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js'),
                        loadScript('https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js'),
                        loadScript('https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js')
                    ]);
                    
                    // Load button feature plugins (depend on core buttons + their dependencies)
                    await Promise.all([
                        loadScript('https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js'),
                        loadScript('https://cdn.datatables.net/buttons/2.4.2/js/buttons.print.min.js')
                    ]);
                    
                    cssPromises.push(loadCSS('https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.min.css'));
                }
                
                // Wait for all CSS to load
                await Promise.all(cssPromises);
                
                // Final verification that jQuery and DataTables are available
                await waitForDataTables();
                
                resolve();
            } catch (error) {
                console.error('Error loading DataTables assets:', error);
                resolve(); // Continue execution even if some assets fail to load
            }
        });
    }
    
    // Helper function to wait for jQuery to be globally available
    function waitForjQuery() {
        return new Promise((resolve) => {
            const checkjQuery = () => {
                if (window.jQuery && typeof window.jQuery === 'function') {
                    resolve();
                } else {
                    setTimeout(checkjQuery, 50);
                }
            };
            checkjQuery();
        });
    }
    
    // Helper function to wait for DataTables to be available
    function waitForDataTables() {
        return new Promise((resolve) => {
            const checkDataTables = () => {
                if (window.jQuery && window.jQuery.fn && window.jQuery.fn.DataTable) {
                    resolve();
                } else {
                    setTimeout(checkDataTables, 50);
                }
            };
            checkDataTables();
        });
    }
    
    function initializeDataTable(tableId, props, wrapper) {
        try {
            const $ = window.jQuery;
            const config = { ...props.datatables_config };
            
            // Add event handlers
            if (props.on_row_click) {
                config.rowCallback = function(row, data, index) {
                    $(row).on('click', function() {
                        // Send event to server
                        if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
                            window.socket.send(JSON.stringify({
                                type: 'event',
                                event: props.on_row_click,
                                data: { row_data: data, row_index: index }
                            }));
                        }
                    });
                };
            }
            
            // Enhance AJAX configuration to support advanced filters
            if (config.ajax && props.pandas_server && props.pandas_server.enabled) {
                const originalAjax = config.ajax;
                const originalDataFunction = typeof originalAjax === 'object' ? originalAjax.data : null;
                const ajaxUrl = typeof originalAjax === 'string' ? originalAjax : originalAjax.url;
                
                config.ajax = {
                    url: ajaxUrl,
                    data: function(d) {
                        console.log('[DEBUG] DataTable AJAX data function called for table:', tableId);
                        console.log('[DEBUG] Original DataTables data:', d);
                        
                        // Call original data function if it exists
                        if (originalDataFunction && typeof originalDataFunction === 'function') {
                            d = originalDataFunction(d) || d;
                            console.log('[DEBUG] After original data function:', d);
                        }
                        
                        // Add advanced filters from global storage
                        const storedFilters = window.cacaoTableFilters && window.cacaoTableFilters[tableId] ?
                            window.cacaoTableFilters[tableId] : {};
                        
                        const filtersJson = JSON.stringify(storedFilters);
                        d.advanced_filters = filtersJson;
                        
                        console.log('[DEBUG] Adding advanced_filters:', filtersJson);
                        console.log('[DEBUG] Final data being sent:', d);
                        
                        return d;
                    }
                };
                
                // Copy other AJAX properties if they exist
                if (typeof originalAjax === 'object') {
                    Object.keys(originalAjax).forEach(key => {
                        if (key !== 'data' && key !== 'url') {
                            config.ajax[key] = originalAjax[key];
                        }
                    });
                }
                
                console.log('[DEBUG] Enhanced AJAX configuration with advanced filters support');
            }
            
            // Initialize DataTable
            const dataTable = $(`#${tableId}`).DataTable(config);
            
            // Store reference for potential future access
            wrapper._dataTable = dataTable;
            
            // Handle server-side events
            if (props.server_side && props.ajax_url) {
                dataTable.on('xhr', function() {
                    console.log('[DataTable] Data loaded from server');
                });
            }
            
            console.log('[CacaoCore] DataTable initialized successfully');
            
        } catch (error) {
            console.error('[CacaoCore] Error initializing DataTable:', error);
            
            // Fallback: create a basic HTML table
            if (!props.server_side && props.dataSource) {
                const tbody = wrapper.querySelector('tbody');
                tbody.innerHTML = '';
                props.dataSource.forEach(row => {
                    const tr = document.createElement('tr');
                    props.columns.forEach(column => {
                        const td = document.createElement('td');
                        const dataIndex = column.dataIndex || column.key;
                        td.textContent = row[dataIndex] || '';
                        tr.appendChild(td);
                    });
                    tbody.appendChild(tr);
                });
            }
        }
    }
    
    function getDataTablesCSS(theme) {
        const baseUrl = 'https://cdn.datatables.net/1.13.7/css/';
        switch (theme) {
            case 'bootstrap5':
                return baseUrl + 'dataTables.bootstrap5.min.css';
            case 'bootstrap4':
                return baseUrl + 'dataTables.bootstrap4.min.css';
            case 'material':
                return baseUrl + 'dataTables.material.min.css';
            default:
                return baseUrl + 'jquery.dataTables.min.css';
        }
    }
    
    function loadScript(src) {
        return new Promise((resolve, reject) => {
            // Check if script already exists
            if (document.querySelector(`script[src="${src}"]`)) {
                resolve();
                return;
            }
            
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    function loadCSS(href) {
        return new Promise((resolve) => {
            // Check if CSS already exists
            if (document.querySelector(`link[href="${href}"]`)) {
                resolve();
                return;
            }
            
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            link.onload = resolve;
            document.head.appendChild(link);
        });
    }
    
    function addFilterToggleButton(wrapper, tableId, props) {
        // Create filter toggle button
        const filterToggle = document.createElement("div");
        filterToggle.className = "table-filter-toggle";
        
        const toggleBtn = document.createElement("button");
        toggleBtn.className = "filter-toggle-btn";
        toggleBtn.innerHTML = `
            <span class="filter-toggle-icon">🔍</span>
            <span>Advanced Filters</span>
            <span class="filter-active-indicator"></span>
        `;
        
        toggleBtn.onclick = () => window.toggleAdvancedFilters(tableId, props);
        
        filterToggle.appendChild(toggleBtn);
        
        // Insert before the table
        wrapper.insertBefore(filterToggle, wrapper.firstChild);
        
        // Store reference for later use
        wrapper._filterToggle = toggleBtn;
    }
    
    // Create wrapper div
    const wrapper = document.createElement("div");
    wrapper.className = isAdvanced ? "datatable-wrapper" : "table-wrapper";
    
    // Create table element
    const table = document.createElement("table");
    table.id = tableId;
    table.className = isAdvanced ? 
        (props.css_classes || "display table table-striped table-hover") : 
        "table";
    
    if (isAdvanced) {
        table.style.width = "100%";
    }
    
    // Create table header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    
    props.columns.forEach(column => {
        const th = document.createElement("th");
        th.textContent = column.title || column.label || "";
        
        if (column.width) {
            th.style.width = column.width;
        }
        
        // Add sorting capability for simple mode
        if (!isAdvanced && props.sorting) {
            th.classList.add("sortable");
            th.onclick = () => {
                console.log("[CacaoCore] Sort by:", column.dataIndex || column.key);
                // Simple sorting logic could be implemented here
            };
        }
        
        headerRow.appendChild(th);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create table body
    const tbody = document.createElement("tbody");
    
    // For simple mode, populate table body immediately
    if (!isAdvanced && Array.isArray(props.dataSource)) {
        props.dataSource.forEach(row => {
            const tr = document.createElement("tr");
            props.columns.forEach(column => {
                const td = document.createElement("td");
                const dataIndex = column.dataIndex || column.key;
                td.textContent = row[dataIndex] || '';
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }
    
    table.appendChild(tbody);
    
    // Create table footer if needed for advanced mode
    if (isAdvanced && props.show_footer) {
        const tfoot = document.createElement("tfoot");
        const footerRow = document.createElement("tr");
        
        props.columns.forEach(column => {
            const th = document.createElement("th");
            th.textContent = column.title || column.label || "";
            footerRow.appendChild(th);
        });
        
        tfoot.appendChild(footerRow);
        table.appendChild(tfoot);
    }
    
    wrapper.appendChild(table);
    
    // Add simple pagination for simple mode
    if (!isAdvanced && props.pagination) {
        const pagination = document.createElement("div");
        pagination.className = "table-pagination";
        
        // Create simple pagination UI
        const paginationInfo = document.createElement("span");
        paginationInfo.className = "pagination-info";
        paginationInfo.textContent = `Page ${props.pagination.current || 1} of ${Math.ceil(props.dataSource.length / (props.pagination.page_size || 10))}`;
        
        const paginationControls = document.createElement("div");
        paginationControls.className = "pagination-controls";
        
        const prevBtn = document.createElement("button");
        prevBtn.textContent = "Previous";
        prevBtn.onclick = () => console.log("[CacaoCore] Previous page");
        
        const nextBtn = document.createElement("button");
        nextBtn.textContent = "Next";
        nextBtn.onclick = () => console.log("[CacaoCore] Next page");
        
        paginationControls.appendChild(prevBtn);
        paginationControls.appendChild(nextBtn);
        
        pagination.appendChild(paginationInfo);
        pagination.appendChild(paginationControls);
        wrapper.appendChild(pagination);
    }
    
    // Advanced mode: Load DataTables.js assets and initialize
    if (isAdvanced) {
        // Add filter toggle button if pandas server is enabled
        if (props.pandas_server && props.pandas_server.enabled) {
            addFilterToggleButton(wrapper, tableId, props);
        }
        
        loadDataTablesAssets(props).then(() => {
            initializeDataTable(tableId, props, wrapper);
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
        window.CacaoCore.componentRenderers['table'] = tableRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: table', error);
    }
})();

// Auto-generated component: tag
(function(){
    try {
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
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
}

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

// Auto-generated component: tree_viewer
(function(){
    try {
        // Helper functions and global definitions
        
        
        // Main component renderer
        const tree_viewerRenderer = (component) => {
    console.log("[CacaoCore] Rendering tree_viewer component:", component);
    const tree = document.createElement('div');
    tree.className = 'tree_viewer';
    
    // Extract props
    const expandAll = component.props.expand_all || false;
    const onNodeClick = component.props.on_node_click;
    const data = component.props.data;
    const theme = component.props.theme || 'light';
    
    // Apply theme class
    tree.classList.add(`theme-${theme}`);
    
    // Set ID if provided
    if (component.props.id) {
        tree.id = component.props.id;
    }

    function renderNode(key, value, parent) {
        const node = document.createElement('div');
        node.className = 'tree-node';
        const isObject = value !== null && typeof value === 'object';

        // toggle handle
        const toggle = document.createElement('span');
        toggle.className = 'tree-expand-toggle';
        toggle.textContent = isObject ? (expandAll ? '▼' : '▶') : '';
        node.appendChild(toggle);

        // key
        const keySpan = document.createElement('span');
        keySpan.className = 'tree-key';
        keySpan.textContent = key;
        node.appendChild(keySpan);

        node.appendChild(document.createTextNode(':'));

        // primitive value
        if (!isObject) {
            const val = document.createElement('span');
            val.className = 'tree-value';
            val.textContent = JSON.stringify(value);
            node.appendChild(val);
        }

        // children
        if (isObject) {
            const childrenWrapper = document.createElement('div');
            childrenWrapper.className = 'tree-children';
            if (!expandAll) {
                childrenWrapper.style.display = 'none';
                node.classList.add('collapsed');
            }
            Object.entries(value).forEach(([k, v]) =>
                renderNode(k, v, childrenWrapper)
            );
            node.appendChild(childrenWrapper);

            toggle.addEventListener('click', () => {
                const collapsed = node.classList.toggle('collapsed');
                childrenWrapper.style.display = collapsed ? 'none' : 'block';
                toggle.textContent = collapsed ? '▶' : '▼';
            });
        }

        // optional click event
        if (onNodeClick) {
            keySpan.style.cursor = 'pointer';
            keySpan.addEventListener('click', () => {
                const evt = new CustomEvent(onNodeClick, { detail: { key } });
                tree.dispatchEvent(evt);
            });
        }

        parent.appendChild(node);
    }

    if (typeof data === 'object' && data !== null) {
        Object.entries(data).forEach(([k, v]) => renderNode(k, v, tree));
    }
    
    return tree;
}

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['tree_viewer'] = tree_viewerRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: tree_viewer', error);
    }
})();

// Auto-generated component: checkbox
(function(){
    try {
        // Helper functions and global definitions
        // Checkbox component renderer
        
        // Main component renderer
        const checkboxRenderer = (component) => {
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
}

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
        // Helper functions and global definitions
        // Datepicker Component Renderer
        
        // Main component renderer
        const datepickerRenderer = (component) => {
    const el = document.createElement("input");
    el.type = "date";
    if (component.props.value) el.value = component.props.value;
    if (component.props.disabled) el.disabled = true;
    if (component.props.style) Object.assign(el.style, component.props.style);
    if (component.props.className) el.className = component.props.className;
    return el;
}

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
        // Helper functions and global definitions
        // Input Component Renderer
        
        // Main component renderer
        const inputRenderer = (component) => {
    const el = document.createElement("input");
    el.type = component.props.inputType || "text";
    el.value = component.props.value || "";
    if (component.props.placeholder) el.placeholder = component.props.placeholder;
    if (component.props.disabled) el.disabled = true;
    if (component.props.style) Object.assign(el.style, component.props.style);
    if (component.props.className) el.className = component.props.className;
    // No onChange binding by default (add if needed)
    return el;
}

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
        // Helper functions and global definitions
        // Radio component renderer
        
        // Main component renderer
        const radioRenderer = (component) => {
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
}

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
}

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
        // Helper functions and global definitions
        // Rate Component Renderer
        
        // Main component renderer
        const rateRenderer = (component) => {
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
        // Helper functions and global definitions
        // Search Component Renderer
        
        // Main component renderer
        const searchRenderer = (component) => {
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
}

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
        // Helper functions and global definitions
        // Select Component Renderer
        
        // Main component renderer
        const selectRenderer = (component) => {
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
}

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
        // Helper functions and global definitions
        // Slider Component Renderer
        
        // Main component renderer
        const sliderRenderer = (component) => {
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
        // Helper functions and global definitions
        // Switch component renderer
        
        // Main component renderer
        const switchRenderer = (component) => {
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
}

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
        // Helper functions and global definitions
        // Textarea Component Renderer
        
        // Main component renderer
        const textareaRenderer = (component) => {
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
}

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
        // Helper functions and global definitions
        // Timepicker Component Renderer
        
        // Main component renderer
        const timepickerRenderer = (component) => {
    const el = document.createElement("input");
    el.type = "time";
    if (component.props.value) el.value = component.props.value;
    if (component.props.disabled) el.disabled = true;
    if (component.props.style) Object.assign(el.style, component.props.style);
    if (component.props.className) el.className = component.props.className;
    return el;
}

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
        // Helper functions and global definitions
        // Upload Component Renderer
        
        // Main component renderer
        const uploadRenderer = (component) => {
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
}

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

// Auto-generated component: breadcrumb
(function(){
    try {
        // Helper functions and global definitions
        // Breadcrumb Component Renderer
        
        // Main component renderer
        const breadcrumbRenderer = (component) => {
  const props = component.props;
  const items = Array.isArray(props.items) ? props.items : [];
  const separator = props.separator || 'arrow';
  const separatorIcon = props.separator_icon;
  const showHome = props.show_home !== false;
  const homeUrl = props.home_url || '/';
  const homeIcon = props.home_icon;
  const maxItems = typeof props.max_items === 'number' ? props.max_items : null;
  const responsive = props.responsive !== false;
  const size = props.size || 'medium';
  const variant = props.variant || 'default';

  // Helper to build separator elements
  function createSeparator() {
    const sep = document.createElement('li');
    sep.className = 'breadcrumb-separator';
    if (separatorIcon) {
      const i = document.createElement('i');
      i.className = `icon-${separatorIcon}`;
      sep.appendChild(i);
    } else if (separator === 'slash') {
      sep.textContent = '/';
    } else if (separator === 'dot') {
      sep.textContent = '•';
    } else {
      // default arrow
      sep.textContent = '>';
    }
    return sep;
  }

  // Build the <nav> wrapper
  const nav = document.createElement('nav');
  nav.className = `breadcrumb breadcrumb--${size} breadcrumb--${variant}` + (responsive ? ' breadcrumb--responsive' : '');
  nav.setAttribute('aria-label', 'breadcrumb');

  // Build the <ol> list
  const ol = document.createElement('ol');
  ol.className = 'breadcrumb-list';

  // Prepare full items array (with home)
  let allItems = [];
  if (showHome) {
    allItems.push({ label: '', url: homeUrl, icon: homeIcon });
  }
  allItems = allItems.concat(items);

  // Handle collapsing if too many items
  let displayItems = allItems;
  if (maxItems && allItems.length > maxItems) {
    const keepStart = Math.ceil(maxItems / 2);
    const keepEnd = Math.floor(maxItems / 2);
    const startSlice = allItems.slice(0, keepStart);
    const endSlice = allItems.slice(allItems.length - keepEnd);
    const overflowSlice = allItems.slice(keepStart, allItems.length - keepEnd);

    displayItems = [
      ...startSlice,
      { label: '…', isOverflow: true, overflowItems: overflowSlice },
      ...endSlice
    ];
  }

  // Render each item (and separators)
  displayItems.forEach((item, idx) => {
    const isLast = idx === displayItems.length - 1;
    const li = document.createElement('li');
    li.className = 'breadcrumb-item';

    if (item.isOverflow) {
      // overflow dropdown
      const drop = document.createElement('span');
      drop.className = 'breadcrumb-overflow';
      drop.textContent = item.label;
      drop.tabIndex = 0;

      const submenu = document.createElement('ul');
      submenu.className = 'breadcrumb-overflow-menu';
      item.overflowItems.forEach(sub => {
        const subLi = document.createElement('li');
        subLi.className = 'breadcrumb-overflow-item';
        if (sub.url) {
          const a = document.createElement('a');
          a.href = sub.url;
          a.textContent = sub.label;
          subLi.appendChild(a);
        } else {
          subLi.textContent = sub.label;
        }
        submenu.appendChild(subLi);
      });

      drop.appendChild(submenu);
      li.appendChild(drop);
    } else {
      // normal item
      if (item.icon && idx === 0 && showHome) {
        const a = document.createElement('a');
        a.href = item.url;
        const i = document.createElement('i');
        i.className = `icon-${item.icon}`;
        a.appendChild(i);
        li.appendChild(a);
      } else if (item.url && !isLast) {
        const a = document.createElement('a');
        a.href = item.url;
        a.textContent = item.label;
        li.appendChild(a);
      } else {
        const span = document.createElement('span');
        span.textContent = item.label;
        li.appendChild(span);
      }
    }

    ol.appendChild(li);

    if (!isLast) {
      ol.appendChild(createSeparator());
    }
  });

  nav.appendChild(ol);
  return nav;
}

        // Ensure the global registry exists
        if (!window.CacaoCore) {
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {};
        }
        if (!window.CacaoCore.componentRenderers) {
            window.CacaoCore.componentRenderers = {};
        }

        // Register the renderer function
        window.CacaoCore.componentRenderers['breadcrumb'] = breadcrumbRenderer;
    } catch (error) {
        console.error('[CacaoComponents] Error registering component: breadcrumb', error);
    }
})();

// Auto-generated component: menu
(function(){
    try {
        // Helper functions and global definitions
        // Menu Component Renderer
        
        // Main component renderer
        const menuRenderer = (component) => {
  const props = component.props;
  const items = Array.isArray(props.items) ? props.items : [];
  const mode = ['horizontal', 'vertical', 'inline'].includes(props.mode) ? props.mode : 'horizontal';
  const theme = props.theme === 'dark' ? 'dark' : 'light';
  const collapsed = props.collapsed === true;
  let selectedKey = props.default_selected || null;

  // Helper to send selection events
  async function sendEvent(eventName, data = {}) {
    if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
      window.socket.send(JSON.stringify({ type: 'event', event: eventName, data }));
    } else {
      let params = `event=${encodeURIComponent(eventName)}&t=${Date.now()}`;
      for (let [k, v] of Object.entries(data)) {
        params += `&${encodeURIComponent(k)}=${encodeURIComponent(v)}`;
      }
      await fetch(`/api/action?${params}`, { method: 'GET' });
    }
  }

  // Create root <ul>
  const root = document.createElement('ul');
  root.className = `menu menu--${mode} menu--${theme}` + (collapsed ? ' menu--collapsed' : '');
  root.setAttribute('role', 'menu');
  root.setAttribute('tabindex', '0');
  root.setAttribute('aria-label', props.ariaLabel || 'Main menu');

  // Keyboard navigation support
  root.addEventListener('keydown', (e) => {
    const itemsEls = Array.from(root.querySelectorAll('.menu-item:not(.is-disabled)'));
    const current = root.querySelector('.menu-item.is-selected');
    let idx = itemsEls.indexOf(current);
    if (e.key === 'ArrowDown' || (e.key === 'ArrowRight' && mode === 'horizontal')) {
      idx = (idx + 1) % itemsEls.length;
      itemsEls[idx].querySelector('button, a').focus();
      e.preventDefault();
    } else if (e.key === 'ArrowUp' || (e.key === 'ArrowLeft' && mode === 'horizontal')) {
      idx = (idx - 1 + itemsEls.length) % itemsEls.length;
      itemsEls[idx].querySelector('button, a').focus();
      e.preventDefault();
    } else if (e.key === 'Home') {
      itemsEls[0].querySelector('button, a').focus();
      e.preventDefault();
    } else if (e.key === 'End') {
      itemsEls[itemsEls.length - 1].querySelector('button, a').focus();
      e.preventDefault();
    }
  });

  // Recursive renderer for each item (and submenu)
  function renderItem(item, container, parentKey = null) {
    const li = document.createElement('li');
    li.className = 'menu-item' + (item.disabled ? ' is-disabled' : '') + (item.key === selectedKey ? ' is-selected' : '');
    li.setAttribute('role', 'menuitem');
    li.setAttribute('tabindex', item.key === selectedKey ? '0' : '-1');
    if (item.key) li.dataset.key = item.key;
    if (item.disabled) li.setAttribute('aria-disabled', 'true');
    if (item.key === selectedKey) li.setAttribute('aria-current', 'true');

    // Icon if present
    if (item.icon) {
      const iconEl = document.createElement('span');
      iconEl.className = 'menu-item__icon';
      iconEl.innerHTML = `<img src="/cacao/core/static/icons/menu.svg" alt="" aria-hidden="true" />`;
      li.appendChild(iconEl);
    }

    // Label (link or button)
    let trigger;
    if (item.url && !item.disabled) {
      trigger = document.createElement('a');
      trigger.href = item.url;
      trigger.className = 'menu-item__link';
      trigger.textContent = item.label || '';
      trigger.setAttribute('tabindex', '-1');
    } else {
      trigger = document.createElement('button');
      trigger.type = 'button';
      trigger.className = 'menu-item__button';
      trigger.textContent = item.label || '';
      if (item.disabled) trigger.disabled = true;
      trigger.setAttribute('tabindex', '-1');
    }
    li.appendChild(trigger);

    // Click handler for selection
    if (!item.disabled) {
      trigger.addEventListener('click', e => {
        e.preventDefault();
        if (selectedKey !== item.key) {
          root.querySelectorAll('.menu-item.is-selected').forEach(el => {
            el.classList.remove('is-selected');
            el.removeAttribute('aria-current');
            el.setAttribute('tabindex', '-1');
          });
          li.classList.add('is-selected');
          li.setAttribute('aria-current', 'true');
          li.setAttribute('tabindex', '0');
          selectedKey = item.key;
          sendEvent(props.on_select || 'menu:select', { key: item.key });
          trigger.focus();
        }
      });
      // Keyboard: Enter/Space selects
      trigger.addEventListener('keydown', e => {
        if ((e.key === 'Enter' || e.key === ' ') && !item.disabled) {
          trigger.click();
        }
      });
    }

    container.appendChild(li);

    // Submenu (children) support
    if (Array.isArray(item.children) && item.children.length) {
      const subUl = document.createElement('ul');
      subUl.className = 'menu-submenu';
      subUl.setAttribute('role', 'menu');
      subUl.setAttribute('aria-label', item.label ? `${item.label} submenu` : 'Submenu');
      item.children.forEach(child => renderItem(child, subUl, item.key));
      li.appendChild(subUl);
      li.setAttribute('aria-haspopup', 'true');
      li.setAttribute('aria-expanded', 'false');
      // Expand/collapse logic could be added here if needed
    }
  }

  // Render all top‑level items
  items.forEach(item => renderItem(item, root));

  // Focus first selected or first item for accessibility
  setTimeout(() => {
    const selected = root.querySelector('.menu-item.is-selected button, .menu-item.is-selected a');
    if (selected) selected.focus();
    else {
      const first = root.querySelector('.menu-item button, .menu-item a');
      if (first) first.focus();
    }
  }, 0);

  return root;
}

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
window.NavbarRenderer = NavbarRenderer;

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
        // Helper functions and global definitions
        // Sidebar component renderer
        
        // Main component renderer
        const nav_itemRenderer = (component) => {
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
}

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
        // Helper functions and global definitions
        
        
        // Main component renderer
        const tabsRenderer = (component) => {
  console.log("[CacaoCore] Rendering tabs component:", component);
  const props = component.props;
  const items = Array.isArray(props.items) ? props.items : [];
  let activeKey = props.active_key || (items[0] && items[0].key) || null;
  const orientation = props.orientation === 'vertical' ? 'vertical' : 'horizontal';
  const size = props.size || 'medium';
  const variant = props.variant || 'default';
  const animated = props.animated !== false;
  const closable = props.closable === true;
  const centered = props.centered === true;
  const showAdd = props.show_add_button === true;
  const maxWidth = props.max_width || null;

  // Helper for sending events (change, close, add)
  async function sendEvent(eventName, data = {}) {
    console.log("[Cacao] Tab event:", eventName, data);
    if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
      window.socket.send(JSON.stringify({ type: 'event', event: eventName, data }));
    } else {
      // HTTP fallback
      let params = `event=${eventName}&t=${Date.now()}`;
      for (const [k,v] of Object.entries(data)) {
        params += `&${encodeURIComponent(k)}=${encodeURIComponent(v)}`;
      }
      await fetch(`/api/action?${params}`, { method: 'GET' });
    }
  }

  // Create root container
  const root = document.createElement('div');
  root.className = `tabs-container tabs-${orientation} tabs-${size} tabs-${variant}`;
  if (centered) root.classList.add('tabs-centered');
  if (animated) root.classList.add('tabs-animated');
  if (closable) root.classList.add('tabs-closable');
  if (showAdd) root.classList.add('tabs-has-add-button');
  if (maxWidth) root.style.maxWidth = maxWidth;

  // Set ID if provided
  if (props.id) {
    root.id = props.id;
  }

  // Create the navigation wrapper
  const nav = document.createElement('div');
  nav.className = 'tabs-nav';

  // Create the tab list
  const list = document.createElement('ul');
  list.className = 'tabs-list';
  list.setAttribute('role', 'tablist');
  if (orientation === 'vertical') {
    list.setAttribute('aria-orientation', 'vertical');
  }

  // Create panels container
  const panels = document.createElement('div');
  panels.className = 'tabs-content';

  // Create indicator for active tab
  const indicator = document.createElement('div');
  indicator.className = 'tabs-indicator';
  nav.appendChild(indicator);

  // Track tab buttons for indicator positioning
  const tabButtons = [];

  // Render each tab + panel
  items.forEach((item, index) => {
    const key = item.key;
    const disabled = item.disabled === true;
    const isActive = key === activeKey;

    // --- Tab Button ---
    const li = document.createElement('li');
    li.className = 'tabs-item';
    
    const btn = document.createElement('button');
    btn.className = `tab-item${isActive ? ' tab-active' : ''}${disabled ? ' tab-disabled' : ''}`;
    btn.setAttribute('role', 'tab');
    btn.setAttribute('aria-selected', isActive);
    btn.setAttribute('aria-controls', `panel-${key}`);
    btn.setAttribute('data-key', key);
    btn.disabled = disabled;
    btn.tabIndex = isActive ? 0 : -1;

    // Tab content wrapper
    const tabContent = document.createElement('div');
    tabContent.className = 'tab-content';

    // Icon
    if (item.icon) {
      const icon = document.createElement('span');
      icon.className = `tab-icon icon-${item.icon}`;
      tabContent.appendChild(icon);
    }

    // Label
    const label = document.createElement('span');
    label.className = 'tab-label';
    label.textContent = item.label || '';
    tabContent.appendChild(label);

    // Badge
    if (item.badge != null) {
      const badge = document.createElement('span');
      badge.className = 'tab-badge';
      badge.textContent = item.badge;
      tabContent.appendChild(badge);
    }

    btn.appendChild(tabContent);

    // Close button
    if (closable && !disabled) {
      const close = document.createElement('button');
      close.className = 'tab-close';
      close.innerHTML = '×';
      close.title = 'Close tab';
      close.setAttribute('aria-label', 'Close tab');
      close.addEventListener('click', e => {
        e.stopPropagation();
        sendEvent(props.on_close || 'tabs:close', { key });
        // remove item & panel
        li.remove();
        panel.remove();
        if (activeKey === key && items.length > 1) {
          // activate first remaining
          const nextKey = root.querySelector('.tab-item:not(.tab-disabled)')?.dataset.key;
          if (nextKey) activateTab(nextKey);
        }
      });
      btn.appendChild(close);
    }

    btn.addEventListener('click', () => {
      if (disabled) return;
      if (key !== activeKey) {
        activateTab(key);
        sendEvent(props.on_change || 'tabs:change', { key });
      }
    });

    li.appendChild(btn);
    list.appendChild(li);
    tabButtons.push(btn);

    // --- Content Panel ---
    const panel = document.createElement('div');
    panel.className = `tab-panel${isActive ? ' tab-panel-active' : ''}`;
    panel.setAttribute('role', 'tabpanel');
    panel.setAttribute('id', `panel-${key}`);
    panel.setAttribute('aria-labelledby', `tab-${key}`);
    panel.setAttribute('data-key', key);
    if (!isActive) panel.hidden = true;
    
    // Handle content - it could be a string or a component
    if (typeof item.content === 'string') {
      panel.innerHTML = item.content;
    } else if (item.content && typeof item.content === 'object') {
      // Render as component
      panel.appendChild(window.CacaoCore.renderComponent(item.content));
    }
    
    panels.appendChild(panel);
  });

  // Optional "Add" button
  if (showAdd) {
    const addLi = document.createElement('li');
    addLi.className = 'tabs-item tabs-item--add';
    const addBtn = document.createElement('button');
    addBtn.className = 'tabs-add-button';
    addBtn.innerHTML = '<span class="tabs-add-icon">+</span>';
    addBtn.title = 'Add tab';
    addBtn.setAttribute('aria-label', 'Add new tab');
    addBtn.addEventListener('click', () => {
      sendEvent(props.on_add || 'tabs:add', {});
    });
    addLi.appendChild(addBtn);
    list.appendChild(addLi);
  }

  nav.appendChild(list);
  root.appendChild(nav);
  root.appendChild(panels);

  // Function to update indicator position
  function updateIndicator() {
    const activeBtn = root.querySelector('.tab-item.tab-active');
    if (activeBtn) {
      const rect = activeBtn.getBoundingClientRect();
      const listRect = list.getBoundingClientRect();
      
      if (orientation === 'horizontal') {
        indicator.style.left = `${activeBtn.offsetLeft}px`;
        indicator.style.width = `${activeBtn.offsetWidth}px`;
        indicator.style.height = '3px';
        indicator.style.top = 'auto';
        indicator.style.bottom = '0';
      } else {
        indicator.style.top = `${activeBtn.offsetTop}px`;
        indicator.style.height = `${activeBtn.offsetHeight}px`;
        indicator.style.width = '3px';
        indicator.style.left = 'auto';
        indicator.style.right = '0';
      }
    }
  }

  // Keyboard navigation
  root.addEventListener('keydown', e => {
    const triggers = Array.from(root.querySelectorAll('.tab-item:not(.tab-disabled)'));
    if (!triggers.length) return;
    
    let currentIndex = triggers.findIndex(t => t.dataset.key === activeKey);
    if (currentIndex === -1) return;
    
    let nextIndex = currentIndex;
    
    switch (e.key) {
      case 'ArrowRight':
        if (orientation === 'horizontal') {
          e.preventDefault();
          nextIndex = (currentIndex + 1) % triggers.length;
        }
        break;
      case 'ArrowLeft':
        if (orientation === 'horizontal') {
          e.preventDefault();
          nextIndex = (currentIndex - 1 + triggers.length) % triggers.length;
        }
        break;
      case 'ArrowDown':
        if (orientation === 'vertical') {
          e.preventDefault();
          nextIndex = (currentIndex + 1) % triggers.length;
        }
        break;
      case 'ArrowUp':
        if (orientation === 'vertical') {
          e.preventDefault();
          nextIndex = (currentIndex - 1 + triggers.length) % triggers.length;
        }
        break;
      case 'Home':
        e.preventDefault();
        nextIndex = 0;
        break;
      case 'End':
        e.preventDefault();
        nextIndex = triggers.length - 1;
        break;
    }
    
    if (nextIndex !== currentIndex) {
      const nextBtn = triggers[nextIndex];
      nextBtn.focus();
      activateTab(nextBtn.dataset.key);
      sendEvent(props.on_change || 'tabs:change', { key: nextBtn.dataset.key });
    }
  });

  // Activate a tab by key
  function activateTab(key) {
    activeKey = key;
    
    // Update tab buttons
    root.querySelectorAll('.tab-item').forEach(btn => {
      const isActive = btn.dataset.key === key;
      btn.classList.toggle('tab-active', isActive);
      btn.setAttribute('aria-selected', isActive);
      btn.tabIndex = isActive ? 0 : -1;
    });
    
    // Update panels
    root.querySelectorAll('.tab-panel').forEach(panel => {
      const isActive = panel.dataset.key === key;
      panel.classList.toggle('tab-panel-active', isActive);
      panel.hidden = !isActive;
    });
    
    // Update indicator position
    updateIndicator();
  }

  // Initial indicator positioning
  setTimeout(() => {
    updateIndicator();
  }, 0);

  // Update indicator on window resize
  window.addEventListener('resize', updateIndicator);

  return root;
}

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
        // Helper functions and global definitions
        // Button Component Renderer
        
        // Main component renderer
        const buttonRenderer = (component) => {
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
}

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
        // Helper functions and global definitions
        // Sidebar component renderer
        
        // Main component renderer
        const sidebarRenderer = (component) => {
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
}

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
        // Helper functions and global definitions
        // Text component renderer
        
        // Main component renderer
        const textRenderer = (component) => {
    const el = document.createElement("p");
    el.className = "text";
    window.CacaoCore.applyContent(el, component.props.content);
    return el;
}

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
