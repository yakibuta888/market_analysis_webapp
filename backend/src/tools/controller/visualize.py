""""""


from tools.models import scraping


def make_graph():
    """データ抽出と可視化を行う"""
    get_tables = scraping.GetTables()
    get_tables.get_data()
