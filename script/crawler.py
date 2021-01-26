from ppomppu_helper import PpomppuHelper

if __name__=="__main__":
    ph = PpomppuHelper()
    prod_details = ph.run()
    ph.save_json(prod_details)