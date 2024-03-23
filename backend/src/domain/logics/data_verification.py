def check_data_status(asset_id, trade_date, session):
    # ここでは SQLAlchemy を使用していると仮定
    settlement = session.query(SettlementModel).filter_by(asset_id=asset_id, trade_date=trade_date).first()
    if settlement:
        return 'final' if settlement.is_final else 'preliminary'
    else:
        return 'not_saved'
