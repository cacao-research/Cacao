/*
 * Auto-generated Cacao Components
 * Generated on: 2025-07-15 00:47:43
 * Components: 14
 *
 * This file extends window.CacaoCore.componentRenderers with compiled components.
 * It must be loaded AFTER cacao-core.js to ensure the global registry exists.
 */


// Auto-generated component: avatar
(function() {
    // Component renderer function
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
        applyContent(icon, component.props.icon);
        el.appendChild(icon);
    }

    return el;
};
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['avatar'] = avatarRenderer;
})();

// Auto-generated component: badge
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['badge'] = badgeRenderer;
})();

// Auto-generated component: card
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['card'] = cardRenderer;
})();

// Auto-generated component: carousel
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['carousel'] = carouselRenderer;
})();

// Auto-generated component: collapse
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['collapse'] = collapseRenderer;
})();

// Auto-generated component: descriptions
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['descriptions'] = descriptionsRenderer;
})();

// Auto-generated component: image
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['image'] = imageRenderer;
})();

// Auto-generated component: list
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['list'] = listRenderer;
})();

// Auto-generated component: plot
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['plot'] = plotRenderer;
})();

// Auto-generated component: popover
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['popover'] = popoverRenderer;
})();

// Auto-generated component: table
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['table'] = tableRenderer;
})();

// Auto-generated component: tag
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['tag'] = tagRenderer;
})();

// Auto-generated component: timeline
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['timeline'] = timelineRenderer;
})();

// Auto-generated component: tooltip
(function() {
    // Component renderer function
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
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['tooltip'] = tooltipRenderer;
})();
