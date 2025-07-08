"""
Navigation page for the components showcase.
Demonstrates navigation components like menu, tabs, breadcrumb, etc.
"""

class NavigationPage:
    def render(self):
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px"
                },
                "children": [
                    {
                        "type": "h1",
                        "props": {
                            "content": "Navigation Components",
                            "style": {
                                "color": "#6B4226",
                                "marginBottom": "20px"
                            }
                        }
                    },
                    # Menu
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Menu",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "menu",
                                    "props": {
                                        "items": [
                                            {"key": "home", "label": "Home"},
                                            {"key": "products", "label": "Products"},
                                            {"key": "about", "label": "About Us"},
                                            {"key": "contact", "label": "Contact"}
                                        ],
                                        "mode": "horizontal",
                                        "selectedKeys": ["home"],
                                        "style": {
                                            "width": "100%"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    # Breadcrumb Example 1
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Breadcrumb Example 1",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "breadcrumb",
                                    "props": {
                                        "items": [
                                            {"label": "Home", "href": "#"},
                                            {"label": "Products", "href": "#"},
                                            {"label": "Electronics", "href": "#"},
                                            {"label": "Smartphones", "href": "#"}
                                        ],
                                        "separator": "/"
                                    }
                                }
                            ]
                        }
                    },
                    # Breadcrumb Example 2
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Breadcrumb Example 2",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "breadcrumb",
                                    "props": {
                                        "items": [
                                            {
                                                "label": "Home",
                                                "href": "#"
                                            },
                                            {
                                                "label": "Products",
                                                "href": "#"
                                            },
                                            {
                                                "label": "Electronics",
                                                "href": "#"
                                            },
                                            {
                                                "label": "Smartphones",
                                                "href": "#"
                                            }
                                        ],
                                        "separator": "/"
                                    }
                                }
                            ]
                        }
                    },
                    # Tabs Example 1
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Tabs Example 1",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "tabs",
                                    "props": {
                                        "items": [
                                            {"key": "tab1", "label": "Tab 1", "content": "Content of Tab 1"},
                                            {"key": "tab2", "label": "Tab 2", "content": "Content of Tab 2"},
                                            {"key": "tab3", "label": "Tab 3", "content": "Content of Tab 3"}
                                        ],
                                        "activeKey": "tab1"
                                    }
                                }
                            ]
                        }
                    },
                    # Tabs Example 2
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Tabs Example 2",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "tabs",
                                    "props": {
                                        "items": [
                                            {
                                                "key": "tab1",
                                                "label": "Description",
                                                "content": "This is a detailed description of the item. It includes important information about features and specifications."
                                            },
                                            {
                                                "key": "tab2",
                                                "label": "Reviews",
                                                "content": "Customer reviews and ratings will be displayed here. Users can read about others' experiences."
                                            },
                                            {
                                                "key": "tab3",
                                                "label": "Shipping",
                                                "content": "Information about shipping options, delivery times, and costs can be found in this section."
                                            }
                                        ],
                                        "activeKey": "tab1"
                                    }
                                }
                            ]
                        }
                    },
                    # Dropdown
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Dropdown",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "dropdown",
                                    "props": {
                                        "items": [
                                            {"key": "1", "label": "Option 1"},
                                            {"key": "2", "label": "Option 2"},
                                            {"key": "3", "label": "Option 3"}
                                        ],
                                        "trigger": "click",
                                        "placement": "bottomLeft",
                                        "children": {
                                            "type": "button",
                                            "props": {
                                                "label": "Click me",
                                                "style": {
                                                    "backgroundColor": "#6B4226",
                                                    "color": "#FFFFFF",
                                                    "border": "none",
                                                    "borderRadius": "4px",
                                                    "padding": "8px 16px",
                                                    "cursor": "pointer"
                                                }
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    # Pagination
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Pagination",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "pagination",
                                    "props": {
                                        "total": 100,
                                        "current": 1,
                                        "pageSize": 10
                                    }
                                }
                            ]
                        }
                    },
                    # Steps
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Steps",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "steps",
                                    "props": {
                                        "items": [
                                            {"key": "1", "label": "Step 1", "content": "First step"},
                                            {"key": "2", "label": "Step 2", "content": "Second step"},
                                            {"key": "3", "label": "Step 3", "content": "Third step"}
                                        ],
                                        "current": 1,
                                        "direction": "horizontal"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }