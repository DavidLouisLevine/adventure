from adventure.response import Response
from adventure.verb import Verb, BuiltInVerbs, ResponseVerb, VerbResponse

noResponseMessage = "That's an odd request"

verbs = BuiltInVerbs((
    ResponseVerb('watch', 'watch', VerbResponse(ifNoObjectResponse=True, message=noResponseMessage, result=Response.IllegalCommand)),
    ResponseVerb('eat', 'eat', VerbResponse(ifNoObjectResponse=True, message=noResponseMessage, result=Response.IllegalCommand)),
    ResponseVerb('sleep', 'sleep', VerbResponse(ifNoObjectResponse=True, message=noResponseMessage, result=Response.IllegalCommand)),
    ResponseVerb('exercise', 'exercise', VerbResponse(ifNoObjectResponse=True, message=noResponseMessage, result=Response.IllegalCommand))),
        f=('GO',))

go = verbs['GO'].MakeResponse
exercise = verbs['exercise'].MakeResponse
watch = verbs['watch'].MakeResponse
eat = verbs['eat'].MakeResponse
sleep = verbs['sleep'].MakeResponse
