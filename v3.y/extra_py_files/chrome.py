from time import sleep

try:
    import undetected_chromedriver as uc
except:
    import pip
    pip.main(['install','undetected_chromedriver'])
    import undetected_chromedriver

for _ in range(1):
    print(__name__)
    input('waiting for end')
    if __name__ == '__main__':
        try:
            driver = uc.Chrome()
        except Exception as e:
            print(repr(e))

input()