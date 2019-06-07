from tasks import add

if __name__ == "__main__":
    s1 = add.s(1, 1)
    s1 = add.s(1, 1)
    s2 = add.s(2)
    s3 = add.s(4)
    s4 = add.s()
    s1.link(s2)
    s2.link(s3)
