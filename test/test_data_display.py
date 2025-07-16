import logging
import pytest
from examples.showcase.data_display_page import DataDisplayPage

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def data_display():
    return DataDisplayPage()

def test_list_component(data_display):
    logger.info("Testing List component rendering")
    rendered = data_display.render()
    list_component = None
    
    for child in rendered["props"]["children"]:
        if child["type"] == "div":
            for subchild in child["props"]["children"]:
                if subchild["type"] == "list":
                    list_component = subchild
                    break
    
    assert list_component is not None, "List component not found"
    logger.debug(f"List items: {list_component['props']['items']}")
    
    assert len(list_component["props"]["items"]) == 3, "List should have 3 items"
    assert list_component["props"]["bordered"] == True, "List should be bordered"
    assert all("title" in item and "description" in item for item in list_component["props"]["items"]), "Items missing title or description"

def test_enhanced_table(data_display):
    logger.info("Testing table component")
    rendered = data_display.render()
    table = None
    
    for child in rendered["props"]["children"]:
        if child["type"] == "div":
            for subchild in child["props"]["children"]:
                if subchild["type"] == "table":
                    table = subchild
                    break
    
    assert table is not None, "table component not found"
    logger.debug(f"Table columns: {table['props']['columns']}")
    logger.debug(f"Table data: {table['props']['dataSource']}")
    
    assert len(table["props"]["columns"]) == 3, "Table should have 3 columns"
    assert len(table["props"]["dataSource"]) == 3, "Table should have 3 data rows"
    assert table["props"]["pagination"]["pageSize"] == 10, "Incorrect page size"
    assert all("key" in item for item in table["props"]["dataSource"]), "Data items missing key property"

def test_card_and_badge(data_display):
    logger.info("Testing Card and Badge components")
    rendered = data_display.render()
    card_with_badge = None
    
    for child in rendered["props"]["children"]:
        if child["type"] == "div":
            logger.debug(f"Checking div child: {child['props'].get('children', [])}")
            for subchild in child["props"].get("children", []):
                if isinstance(subchild, dict) and subchild["type"] == "div":
                    for card in subchild["props"].get("children", []):
                        if card["type"] == "card" and "Card with Badge" in str(card["props"]["title"]):
                            card_with_badge = card
                            break
    
    assert card_with_badge is not None, "Card with Badge not found"
    logger.debug(f"Card title: {card_with_badge['props']['title']}")
    
    badge = card_with_badge["props"]["children"]
    assert badge["type"] == "badge", "Badge component not found in card"
    assert badge["props"]["count"] == 5, "Incorrect badge count"
    assert badge["props"]["children"]["type"] == "div", "Badge content structure incorrect"

def test_avatar_and_tags(data_display):
    logger.info("Testing Avatar and Tag components")
    rendered = data_display.render()
    avatar_section = None
    
    # Debug log the entire structure
    logger.debug("Searching for Avatar & Tags section in structure:")
    for child in rendered["props"]["children"]:
        if child["type"] == "div":
            logger.debug(f"Found div with children: {child['props'].get('children', [])}")
            for subchild in child["props"].get("children", []):
                if isinstance(subchild, dict):
                    logger.debug(f"Checking subchild: {subchild.get('type', 'unknown')}")
                    if subchild["type"] == "div":
                        # Look for the h4 title
                        for item in subchild["props"].get("children", []):
                            if item.get("type") == "h4" and "content" in item["props"]:
                                logger.debug(f"Found h4 with content: {item['props']['content']}")
                                if item["props"]["content"] == "Avatar & Tags":
                                    avatar_section = subchild
                                    break
    
    assert avatar_section is not None, "Avatar section not found"
    logger.debug(f"Avatar section structure: {avatar_section}")
    
    # Find avatar and tags components
    avatar = None
    tags = []
    
    def find_components(node):
        nonlocal avatar, tags
        if isinstance(node, dict):
            if node.get("type") == "avatar":
                avatar = node
            elif node.get("type") == "tag":
                tags.append(node)
            
            # Recursively search children
            children = node.get("props", {}).get("children", [])
            if isinstance(children, list):
                for child in children:
                    find_components(child)
            else:
                find_components(children)
    
    find_components(avatar_section)
    
    assert avatar is not None, "Avatar component not found"
    logger.debug(f"Avatar props: {avatar['props']}")
    logger.debug(f"Found {len(tags)} tags: {tags}")
    
    assert len(tags) == 2, "Expected 2 tags"
    assert tags[0]["props"]["color"] == "blue", "First tag should be blue"
    assert tags[1]["props"]["color"] == "green", "Second tag should be green"

def test_timeline(data_display):
    logger.info("Testing Timeline component")
    rendered = data_display.render()
    timeline = None
    
    # Debug log the structure
    logger.debug("Searching for Timeline component in structure:")
    for child in rendered["props"]["children"]:
        if child["type"] == "div":
            logger.debug(f"Checking div children:")
            for subchild in child["props"].get("children", []):
                if isinstance(subchild, dict):
                    logger.debug(f"Found child of type: {subchild.get('type', 'unknown')}")
                    for item in subchild["props"].get("children", []):
                        if isinstance(item, dict):
                            logger.debug(f"Checking item: {item.get('type', 'unknown')}")
                            if item["type"] == "timeline":
                                timeline = item
                                break
    
    assert timeline is not None, "Timeline component not found"
    logger.debug(f"Timeline structure: {timeline}")
    
    assert timeline["props"]["mode"] == "left", "Timeline mode should be 'left'"
    assert len(timeline["props"]["items"]) == 3, "Timeline should have 3 items"
    assert all("label" in item and "content" in item for item in timeline["props"]["items"]), "Timeline items missing label or content"