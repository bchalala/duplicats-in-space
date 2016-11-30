def removeQuotations(titleString):
    """ Remove the extra " in a given paper title. """

    ## I'm honestly not sure if this is necessary. 
    ## This is covered in AuthorParserHelper already
    titleString = titleString.replace('"', "")

    return titleString


def checkWhenLessThan3(titleString):
    """ check if the paper has less than three words. """
    spaceCounter = 0
    for character in titleString:
        if character == ' ':
            spaceCounter += 1

    if spaceCounter<3:
        return True

    return False
