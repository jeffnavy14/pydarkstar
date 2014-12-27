"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
from pydarkstar.tables.auction_house import AuctionHouse
import sqlalchemy.exc
import logging

def getStock(session, itemid, stack=False, seller=None):
    """
    Query for the number of items currently being sold.

    :param session: session object created from database
    :param itemid: item number
    :param stack: consider stacks
    :param seller: consider seller

    :type session: py:class:`pydarkstar.database._Session`
    :type itemid: int
    :type stack: int
    :type seller: int
    """
    try:
        # make sure stack is an int
        if stack:
            stack = 1
        else:
            stack = 0

        # ignore seller
        if seller is None:
            N = session.query(AuctionHouse).filter(
                AuctionHouse.itemid == itemid,
                AuctionHouse.stack  == stack,
                AuctionHouse.sale   == 0,
            ).count()

        # consider seller
        else:

            # make sure seller is valid
            assert isinstance(seller, int)
            assert seller >= 0

            N = session.query(AuctionHouse).filter(
                AuctionHouse.itemid == itemid,
                AuctionHouse.seller == seller,
                AuctionHouse.stack  == stack,
                AuctionHouse.sale   == 0,
            ).count()

        # return count
        return N

    except sqlalchemy.exc.SQLAlchemyError:
        logging.exception('getStock has failed')

    except AssertionError:
        logging.exception('getStock has failed')

    # return invalid count
    return 99999

def getPrice(session, itemid, stack=False, seller=None, func=min):
    """
    Query for the price of an item.

    :param session: session object created from database
    :param itemid: item number
    :param stack: consider stacks
    :param seller: consider seller
    :param func: processing function

    :type session: py:class:`pydarkstar.database._Session`
    :type itemid: int
    :type stack: int
    :type seller: int
    :type func: lambda
    """
    try:
        # make sure stack is an int
        if stack:
            stack = 1
        else:
            stack = 0

        # ignore seller
        if seller is None:
            N = func(
                session.query(AuctionHouse.sale).filter(
                    AuctionHouse.itemid == itemid,
                    AuctionHouse.stack  == stack,
                    AuctionHouse.sale   != 0,
            ))

        # consider seller
        else:

            # make sure seller is valid
            assert isinstance(seller, int)
            assert seller >= 0

            N = func(
                session.query(AuctionHouse.sale).filter(
                    AuctionHouse.itemid == itemid,
                    AuctionHouse.seller == seller,
                    AuctionHouse.stack  == stack,
                    AuctionHouse.sale   != 0,
            ))

        # return price
        return N

    except sqlalchemy.exc.SQLAlchemyError:
        logging.exception('getPrice has failed')

    except AssertionError:
        logging.exception('getPrice has failed')

    # return invalid price
    return -1

if __name__ == '__main__':
    pass