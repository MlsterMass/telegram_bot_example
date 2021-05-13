import pyqrcode


def qr_link(link):
    qr = pyqrcode.create(link, "L")
    qr.png("documents/qr_btc_link.png", scale=6)
    file = open("documents/qr_btc_link.png", "rb")
    return file



