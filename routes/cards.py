from fastapi import APIRouter
from data.cards_data import CARDS_DATA
from data.popular_cards_data import POPULAR_CARDS_DATA

router = APIRouter()

@router.get("/cards")
def get_cards():
    """모든 카드 정보를 반환합니다."""
    return {
        "success": True,
        "data": CARDS_DATA
    }

@router.get("/popular-cards")
def get_popular_cards():
    """인기 카드 정보를 반환합니다."""
    return {
        "success": True,
        "data": {
            "popularCards": POPULAR_CARDS_DATA
        }
    } 