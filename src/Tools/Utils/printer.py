import traceback

from typing import Dict, Union

from discord.ext.commands.context import Context

from Tools.Extractor.ctx_extractor import ContextExtractor

from Data.Cache.errorcode import ERROR_CODE


Dictx = Dict[str, Union[str, int, None]]


''' __doc_var__=ERO % format %
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    CollieInfo has been already allocated but reallocation has been executed
        {
            __info: Info = {
                "__id__" : % Not None %,
                "__name__"  : % Not None %
            }

            if cls.__id__ == None and cls.__name__ == None:
                ...
            else
    ----------> raise ReallocationException(...)
        }
    Raising ReallocationException

Already allocated(__id__: 4566485465, __name__: None)

+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Traceback (most recent call last):
  File "% path %", line N, in <module>
    CollieInfo.assign(**info)
  File "% path %", line N, in assign
    raise ReallocationException(cls.__info["__id__"], cls.__info["__name__"])
Temp.errors.exceptions.ReallocationException: Already allocated(__id__: 4566485465, __name__: None)

+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
% !end format %
'''
def print_ERO(ERO: Exception, *args) -> None:
    LINE = "\n" + "+-+-" * 25 + "+"
    
    print(LINE)
    
    if args:
        for _Emsg in args:
            print("\n" + _Emsg)
        else:
            print(LINE)
    
    __ero_cls_name__ = ERO.__class__.__name__
    
    if __ero_cls_name__ in ERROR_CODE:
        print(f"BorderCollie Error_code({ERROR_CODE.get(__ero_cls_name__)}) occured")
    else:
        print(f"Default Exception ({__ero_cls_name__}) occured")
    
    print(ERO.__doc__, ERO, sep="\n\n")
    
    print(LINE + "\n")
    
    traceback.print_exc()

    print(LINE + "\n")
    

    
''' __doc_var__=Dictx % format %
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

dictx = {

    SI:     server_id                               # int
    SN:     server_name                             # str
    CN:     commander_name                          # str
    CI:     commander_id                            # int
    CETCN:  commander_executed_text_channel_name    # str
    CETCI:  commander_executed_text_channel_id      # int
    CEVCN:  commander_entered_voice_channel_name    # Optional[str]
    CEVCI:  commander_entered_voice_channel_id      # Optional[int]
    BEVCN:  bot_entered_voice_channel_name          # Optional[str]
    BEVCI:  bot_entered_voice_channel_id            # Optional[int]
}

+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
% !end format %
'''
def print_Dictx(dictx: Dictx) -> None:
    print("\n" + "+-+-" * 25 + "+\n")
    
    print("dictx = {\n")
    
    for k, v in dictx.items():
        print(f"    {k}: {v}")
    else:
        print("}")
      
    print("\n" + "+-+-" * 25 + "+\n")
    

    
'''
__doc_var__=Dictx
'''
def print_context(ctx: Context) -> None:
    summrized: Dictx = ContextExtractor.summarize(ctx)
    
    print_Dictx(summrized)
