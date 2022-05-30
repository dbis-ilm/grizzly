# Generated from grammar/Python3d3.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


from antlr4.Token import CommonToken
import re
import importlib
# Allow languages to extend the lexer and parser, by loading the parser dynamically
module_path = __name__[:-5]
language_name = __name__.split('.')[-1]
language_name = language_name[:-5]  # Remove Lexer from name
LanguageParser = getattr(importlib.import_module('{}Parser'.format(module_path)), '{}Parser'.format(language_name))



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2C")
        buf.write("\u01db\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\3\2\3\2\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3")
        buf.write("\5\3\5\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\7")
        buf.write("\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\f\3\f\3\f\3\r")
        buf.write("\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3")
        buf.write("\16\3\17\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\20")
        buf.write("\3\20\3\20\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\23\3\23")
        buf.write("\3\23\3\23\3\24\3\24\3\25\3\25\3\26\3\26\3\26\3\27\3\27")
        buf.write("\3\27\3\30\3\30\3\30\3\31\3\31\3\31\3\32\3\32\3\33\3\33")
        buf.write("\3\34\3\34\3\35\3\35\3\36\3\36\3\37\3\37\3\37\3 \3 \3")
        buf.write("!\3!\3\"\3\"\3#\3#\3$\3$\3$\3%\3%\3%\3&\3&\3\'\3\'\3\'")
        buf.write("\3\'\3\'\3\'\3\'\3(\3(\3(\3)\3)\3)\3)\3*\3*\3*\3*\3+\3")
        buf.write("+\3+\3+\3+\3,\3,\3,\3,\3,\3,\3-\3-\3-\3-\3-\3.\3.\3.\3")
        buf.write(".\3.\3/\3/\3\60\3\60\3\61\3\61\3\62\7\62\u014b\n\62\f")
        buf.write("\62\16\62\u014e\13\62\3\62\3\62\7\62\u0152\n\62\f\62\16")
        buf.write("\62\u0155\13\62\3\63\3\63\3\63\3\63\3\63\3\63\3\63\3\63")
        buf.write("\3\63\5\63\u0160\n\63\3\64\3\64\3\65\3\65\3\65\5\65\u0167")
        buf.write("\n\65\3\65\3\65\5\65\u016b\n\65\3\65\5\65\u016e\n\65\5")
        buf.write("\65\u0170\n\65\3\65\3\65\3\66\3\66\3\66\3\66\6\66\u0178")
        buf.write("\n\66\r\66\16\66\u0179\3\67\3\67\7\67\u017e\n\67\f\67")
        buf.write("\16\67\u0181\13\67\38\38\78\u0185\n8\f8\168\u0188\138")
        buf.write("\38\38\38\78\u018d\n8\f8\168\u0190\138\38\58\u0193\n8")
        buf.write("\39\39\79\u0197\n9\f9\169\u019a\139\39\69\u019d\n9\r9")
        buf.write("\169\u019e\59\u01a1\n9\3:\3:\3;\3;\3<\3<\3=\3=\3>\3>\3")
        buf.write("?\3?\3@\3@\3A\3A\3A\5A\u01b4\nA\3A\3A\3B\3B\3C\3C\3D\3")
        buf.write("D\3E\6E\u01bf\nE\rE\16E\u01c0\3F\3F\7F\u01c5\nF\fF\16")
        buf.write("F\u01c8\13F\3G\3G\5G\u01cc\nG\3G\5G\u01cf\nG\3G\3G\5G")
        buf.write("\u01d3\nG\3H\5H\u01d6\nH\3I\3I\5I\u01da\nI\4\u0186\u018e")
        buf.write("\2J\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r")
        buf.write("\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30")
        buf.write("/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'")
        buf.write("M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q")
        buf.write(":s;u<w=y>{?}@\177A\u0081B\u0083C\u0085\2\u0087\2\u0089")
        buf.write("\2\u008b\2\u008d\2\u008f\2\u0091\2\3\2\7\3\2\63;\3\2\62")
        buf.write(";\4\2\13\13\"\"\4\2\f\f\16\17\5\2C\\aac|\2\u01ea\2\3\3")
        buf.write("\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2")
        buf.write("\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2")
        buf.write("\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2")
        buf.write("\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2")
        buf.write("\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3")
        buf.write("\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2")
        buf.write("\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3")
        buf.write("\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K")
        buf.write("\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2")
        buf.write("U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2")
        buf.write("\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2")
        buf.write("\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2")
        buf.write("\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3")
        buf.write("\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083")
        buf.write("\3\2\2\2\3\u0093\3\2\2\2\5\u0095\3\2\2\2\7\u009b\3\2\2")
        buf.write("\2\t\u00a4\3\2\2\2\13\u00ab\3\2\2\2\r\u00b1\3\2\2\2\17")
        buf.write("\u00b4\3\2\2\2\21\u00b9\3\2\2\2\23\u00be\3\2\2\2\25\u00c4")
        buf.write("\3\2\2\2\27\u00c8\3\2\2\2\31\u00cb\3\2\2\2\33\u00d0\3")
        buf.write("\2\2\2\35\u00d8\3\2\2\2\37\u00de\3\2\2\2!\u00e4\3\2\2")
        buf.write("\2#\u00e8\3\2\2\2%\u00eb\3\2\2\2\'\u00ef\3\2\2\2)\u00f1")
        buf.write("\3\2\2\2+\u00f3\3\2\2\2-\u00f6\3\2\2\2/\u00f9\3\2\2\2")
        buf.write("\61\u00fc\3\2\2\2\63\u00ff\3\2\2\2\65\u0101\3\2\2\2\67")
        buf.write("\u0103\3\2\2\29\u0105\3\2\2\2;\u0107\3\2\2\2=\u0109\3")
        buf.write("\2\2\2?\u010c\3\2\2\2A\u010e\3\2\2\2C\u0110\3\2\2\2E\u0112")
        buf.write("\3\2\2\2G\u0114\3\2\2\2I\u0117\3\2\2\2K\u011a\3\2\2\2")
        buf.write("M\u011c\3\2\2\2O\u0123\3\2\2\2Q\u0126\3\2\2\2S\u012a\3")
        buf.write("\2\2\2U\u012e\3\2\2\2W\u0133\3\2\2\2Y\u0139\3\2\2\2[\u013e")
        buf.write("\3\2\2\2]\u0143\3\2\2\2_\u0145\3\2\2\2a\u0147\3\2\2\2")
        buf.write("c\u014c\3\2\2\2e\u015f\3\2\2\2g\u0161\3\2\2\2i\u016f\3")
        buf.write("\2\2\2k\u0173\3\2\2\2m\u017b\3\2\2\2o\u0192\3\2\2\2q\u01a0")
        buf.write("\3\2\2\2s\u01a2\3\2\2\2u\u01a4\3\2\2\2w\u01a6\3\2\2\2")
        buf.write("y\u01a8\3\2\2\2{\u01aa\3\2\2\2}\u01ac\3\2\2\2\177\u01ae")
        buf.write("\3\2\2\2\u0081\u01b3\3\2\2\2\u0083\u01b7\3\2\2\2\u0085")
        buf.write("\u01b9\3\2\2\2\u0087\u01bb\3\2\2\2\u0089\u01be\3\2\2\2")
        buf.write("\u008b\u01c2\3\2\2\2\u008d\u01c9\3\2\2\2\u008f\u01d5\3")
        buf.write("\2\2\2\u0091\u01d9\3\2\2\2\u0093\u0094\7<\2\2\u0094\4")
        buf.write("\3\2\2\2\u0095\u0096\7d\2\2\u0096\u0097\7t\2\2\u0097\u0098")
        buf.write("\7g\2\2\u0098\u0099\7c\2\2\u0099\u009a\7m\2\2\u009a\6")
        buf.write("\3\2\2\2\u009b\u009c\7e\2\2\u009c\u009d\7q\2\2\u009d\u009e")
        buf.write("\7p\2\2\u009e\u009f\7v\2\2\u009f\u00a0\7k\2\2\u00a0\u00a1")
        buf.write("\7p\2\2\u00a1\u00a2\7w\2\2\u00a2\u00a3\7g\2\2\u00a3\b")
        buf.write("\3\2\2\2\u00a4\u00a5\7t\2\2\u00a5\u00a6\7g\2\2\u00a6\u00a7")
        buf.write("\7v\2\2\u00a7\u00a8\7w\2\2\u00a8\u00a9\7t\2\2\u00a9\u00aa")
        buf.write("\7p\2\2\u00aa\n\3\2\2\2\u00ab\u00ac\7t\2\2\u00ac\u00ad")
        buf.write("\7c\2\2\u00ad\u00ae\7k\2\2\u00ae\u00af\7u\2\2\u00af\u00b0")
        buf.write("\7g\2\2\u00b0\f\3\2\2\2\u00b1\u00b2\7k\2\2\u00b2\u00b3")
        buf.write("\7h\2\2\u00b3\16\3\2\2\2\u00b4\u00b5\7g\2\2\u00b5\u00b6")
        buf.write("\7n\2\2\u00b6\u00b7\7k\2\2\u00b7\u00b8\7h\2\2\u00b8\20")
        buf.write("\3\2\2\2\u00b9\u00ba\7g\2\2\u00ba\u00bb\7n\2\2\u00bb\u00bc")
        buf.write("\7u\2\2\u00bc\u00bd\7g\2\2\u00bd\22\3\2\2\2\u00be\u00bf")
        buf.write("\7y\2\2\u00bf\u00c0\7j\2\2\u00c0\u00c1\7k\2\2\u00c1\u00c2")
        buf.write("\7n\2\2\u00c2\u00c3\7g\2\2\u00c3\24\3\2\2\2\u00c4\u00c5")
        buf.write("\7h\2\2\u00c5\u00c6\7q\2\2\u00c6\u00c7\7t\2\2\u00c7\26")
        buf.write("\3\2\2\2\u00c8\u00c9\7k\2\2\u00c9\u00ca\7p\2\2\u00ca\30")
        buf.write("\3\2\2\2\u00cb\u00cc\7v\2\2\u00cc\u00cd\7t\2\2\u00cd\u00ce")
        buf.write("\7{\2\2\u00ce\u00cf\7<\2\2\u00cf\32\3\2\2\2\u00d0\u00d1")
        buf.write("\7h\2\2\u00d1\u00d2\7k\2\2\u00d2\u00d3\7p\2\2\u00d3\u00d4")
        buf.write("\7c\2\2\u00d4\u00d5\7n\2\2\u00d5\u00d6\7n\2\2\u00d6\u00d7")
        buf.write("\7{\2\2\u00d7\34\3\2\2\2\u00d8\u00d9\7t\2\2\u00d9\u00da")
        buf.write("\7c\2\2\u00da\u00db\7p\2\2\u00db\u00dc\7i\2\2\u00dc\u00dd")
        buf.write("\7g\2\2\u00dd\36\3\2\2\2\u00de\u00df\7r\2\2\u00df\u00e0")
        buf.write("\7t\2\2\u00e0\u00e1\7k\2\2\u00e1\u00e2\7p\2\2\u00e2\u00e3")
        buf.write("\7v\2\2\u00e3 \3\2\2\2\u00e4\u00e5\7c\2\2\u00e5\u00e6")
        buf.write("\7p\2\2\u00e6\u00e7\7f\2\2\u00e7\"\3\2\2\2\u00e8\u00e9")
        buf.write("\7q\2\2\u00e9\u00ea\7t\2\2\u00ea$\3\2\2\2\u00eb\u00ec")
        buf.write("\7p\2\2\u00ec\u00ed\7q\2\2\u00ed\u00ee\7v\2\2\u00ee&\3")
        buf.write("\2\2\2\u00ef\u00f0\7>\2\2\u00f0(\3\2\2\2\u00f1\u00f2\7")
        buf.write("@\2\2\u00f2*\3\2\2\2\u00f3\u00f4\7?\2\2\u00f4\u00f5\7")
        buf.write("?\2\2\u00f5,\3\2\2\2\u00f6\u00f7\7@\2\2\u00f7\u00f8\7")
        buf.write("?\2\2\u00f8.\3\2\2\2\u00f9\u00fa\7>\2\2\u00fa\u00fb\7")
        buf.write("?\2\2\u00fb\60\3\2\2\2\u00fc\u00fd\7#\2\2\u00fd\u00fe")
        buf.write("\7?\2\2\u00fe\62\3\2\2\2\u00ff\u0100\7-\2\2\u0100\64\3")
        buf.write("\2\2\2\u0101\u0102\7/\2\2\u0102\66\3\2\2\2\u0103\u0104")
        buf.write("\7,\2\2\u01048\3\2\2\2\u0105\u0106\7\61\2\2\u0106:\3\2")
        buf.write("\2\2\u0107\u0108\7\'\2\2\u0108<\3\2\2\2\u0109\u010a\7")
        buf.write(",\2\2\u010a\u010b\7,\2\2\u010b>\3\2\2\2\u010c\u010d\7")
        buf.write("(\2\2\u010d@\3\2\2\2\u010e\u010f\7~\2\2\u010fB\3\2\2\2")
        buf.write("\u0110\u0111\7\u0080\2\2\u0111D\3\2\2\2\u0112\u0113\7")
        buf.write("`\2\2\u0113F\3\2\2\2\u0114\u0115\7>\2\2\u0115\u0116\7")
        buf.write(">\2\2\u0116H\3\2\2\2\u0117\u0118\7@\2\2\u0118\u0119\7")
        buf.write("@\2\2\u0119J\3\2\2\2\u011a\u011b\7\60\2\2\u011bL\3\2\2")
        buf.write("\2\u011c\u011d\7g\2\2\u011d\u011e\7z\2\2\u011e\u011f\7")
        buf.write("e\2\2\u011f\u0120\7g\2\2\u0120\u0121\7r\2\2\u0121\u0122")
        buf.write("\7v\2\2\u0122N\3\2\2\2\u0123\u0124\7c\2\2\u0124\u0125")
        buf.write("\7u\2\2\u0125P\3\2\2\2\u0126\u0127\7k\2\2\u0127\u0128")
        buf.write("\7p\2\2\u0128\u0129\7v\2\2\u0129R\3\2\2\2\u012a\u012b")
        buf.write("\7u\2\2\u012b\u012c\7v\2\2\u012c\u012d\7t\2\2\u012dT\3")
        buf.write("\2\2\2\u012e\u012f\7n\2\2\u012f\u0130\7k\2\2\u0130\u0131")
        buf.write("\7u\2\2\u0131\u0132\7v\2\2\u0132V\3\2\2\2\u0133\u0134")
        buf.write("\7h\2\2\u0134\u0135\7n\2\2\u0135\u0136\7q\2\2\u0136\u0137")
        buf.write("\7c\2\2\u0137\u0138\7v\2\2\u0138X\3\2\2\2\u0139\u013a")
        buf.write("\7d\2\2\u013a\u013b\7q\2\2\u013b\u013c\7q\2\2\u013c\u013d")
        buf.write("\7n\2\2\u013dZ\3\2\2\2\u013e\u013f\7P\2\2\u013f\u0140")
        buf.write("\7q\2\2\u0140\u0141\7p\2\2\u0141\u0142\7g\2\2\u0142\\")
        buf.write("\3\2\2\2\u0143\u0144\7.\2\2\u0144^\3\2\2\2\u0145\u0146")
        buf.write("\5o8\2\u0146`\3\2\2\2\u0147\u0148\5g\64\2\u0148b\3\2\2")
        buf.write("\2\u0149\u014b\5\u0087D\2\u014a\u0149\3\2\2\2\u014b\u014e")
        buf.write("\3\2\2\2\u014c\u014a\3\2\2\2\u014c\u014d\3\2\2\2\u014d")
        buf.write("\u014f\3\2\2\2\u014e\u014c\3\2\2\2\u014f\u0153\7\60\2")
        buf.write("\2\u0150\u0152\5\u0087D\2\u0151\u0150\3\2\2\2\u0152\u0155")
        buf.write("\3\2\2\2\u0153\u0151\3\2\2\2\u0153\u0154\3\2\2\2\u0154")
        buf.write("d\3\2\2\2\u0155\u0153\3\2\2\2\u0156\u0157\7V\2\2\u0157")
        buf.write("\u0158\7t\2\2\u0158\u0159\7w\2\2\u0159\u0160\7g\2\2\u015a")
        buf.write("\u015b\7H\2\2\u015b\u015c\7c\2\2\u015c\u015d\7n\2\2\u015d")
        buf.write("\u015e\7u\2\2\u015e\u0160\7g\2\2\u015f\u0156\3\2\2\2\u015f")
        buf.write("\u015a\3\2\2\2\u0160f\3\2\2\2\u0161\u0162\5q9\2\u0162")
        buf.write("h\3\2\2\2\u0163\u0164\6\65\2\2\u0164\u0170\5\u0089E\2")
        buf.write("\u0165\u0167\7\17\2\2\u0166\u0165\3\2\2\2\u0166\u0167")
        buf.write("\3\2\2\2\u0167\u0168\3\2\2\2\u0168\u016b\7\f\2\2\u0169")
        buf.write("\u016b\4\16\17\2\u016a\u0166\3\2\2\2\u016a\u0169\3\2\2")
        buf.write("\2\u016b\u016d\3\2\2\2\u016c\u016e\5\u0089E\2\u016d\u016c")
        buf.write("\3\2\2\2\u016d\u016e\3\2\2\2\u016e\u0170\3\2\2\2\u016f")
        buf.write("\u0163\3\2\2\2\u016f\u016a\3\2\2\2\u0170\u0171\3\2\2\2")
        buf.write("\u0171\u0172\b\65\2\2\u0172j\3\2\2\2\u0173\u0174\7i\2")
        buf.write("\2\u0174\u0175\7a\2\2\u0175\u0177\3\2\2\2\u0176\u0178")
        buf.write("\5\u0091I\2\u0177\u0176\3\2\2\2\u0178\u0179\3\2\2\2\u0179")
        buf.write("\u0177\3\2\2\2\u0179\u017a\3\2\2\2\u017al\3\2\2\2\u017b")
        buf.write("\u017f\5\u008fH\2\u017c\u017e\5\u0091I\2\u017d\u017c\3")
        buf.write("\2\2\2\u017e\u0181\3\2\2\2\u017f\u017d\3\2\2\2\u017f\u0180")
        buf.write("\3\2\2\2\u0180n\3\2\2\2\u0181\u017f\3\2\2\2\u0182\u0186")
        buf.write("\7$\2\2\u0183\u0185\13\2\2\2\u0184\u0183\3\2\2\2\u0185")
        buf.write("\u0188\3\2\2\2\u0186\u0187\3\2\2\2\u0186\u0184\3\2\2\2")
        buf.write("\u0187\u0189\3\2\2\2\u0188\u0186\3\2\2\2\u0189\u0193\7")
        buf.write("$\2\2\u018a\u018e\7)\2\2\u018b\u018d\13\2\2\2\u018c\u018b")
        buf.write("\3\2\2\2\u018d\u0190\3\2\2\2\u018e\u018f\3\2\2\2\u018e")
        buf.write("\u018c\3\2\2\2\u018f\u0191\3\2\2\2\u0190\u018e\3\2\2\2")
        buf.write("\u0191\u0193\7)\2\2\u0192\u0182\3\2\2\2\u0192\u018a\3")
        buf.write("\2\2\2\u0193p\3\2\2\2\u0194\u0198\5\u0085C\2\u0195\u0197")
        buf.write("\5\u0087D\2\u0196\u0195\3\2\2\2\u0197\u019a\3\2\2\2\u0198")
        buf.write("\u0196\3\2\2\2\u0198\u0199\3\2\2\2\u0199\u01a1\3\2\2\2")
        buf.write("\u019a\u0198\3\2\2\2\u019b\u019d\7\62\2\2\u019c\u019b")
        buf.write("\3\2\2\2\u019d\u019e\3\2\2\2\u019e\u019c\3\2\2\2\u019e")
        buf.write("\u019f\3\2\2\2\u019f\u01a1\3\2\2\2\u01a0\u0194\3\2\2\2")
        buf.write("\u01a0\u019c\3\2\2\2\u01a1r\3\2\2\2\u01a2\u01a3\7*\2\2")
        buf.write("\u01a3t\3\2\2\2\u01a4\u01a5\7+\2\2\u01a5v\3\2\2\2\u01a6")
        buf.write("\u01a7\7]\2\2\u01a7x\3\2\2\2\u01a8\u01a9\7_\2\2\u01a9")
        buf.write("z\3\2\2\2\u01aa\u01ab\7}\2\2\u01ab|\3\2\2\2\u01ac\u01ad")
        buf.write("\7\177\2\2\u01ad~\3\2\2\2\u01ae\u01af\7?\2\2\u01af\u0080")
        buf.write("\3\2\2\2\u01b0\u01b4\5\u0089E\2\u01b1\u01b4\5\u008bF\2")
        buf.write("\u01b2\u01b4\5\u008dG\2\u01b3\u01b0\3\2\2\2\u01b3\u01b1")
        buf.write("\3\2\2\2\u01b3\u01b2\3\2\2\2\u01b4\u01b5\3\2\2\2\u01b5")
        buf.write("\u01b6\bA\3\2\u01b6\u0082\3\2\2\2\u01b7\u01b8\13\2\2\2")
        buf.write("\u01b8\u0084\3\2\2\2\u01b9\u01ba\t\2\2\2\u01ba\u0086\3")
        buf.write("\2\2\2\u01bb\u01bc\t\3\2\2\u01bc\u0088\3\2\2\2\u01bd\u01bf")
        buf.write("\t\4\2\2\u01be\u01bd\3\2\2\2\u01bf\u01c0\3\2\2\2\u01c0")
        buf.write("\u01be\3\2\2\2\u01c0\u01c1\3\2\2\2\u01c1\u008a\3\2\2\2")
        buf.write("\u01c2\u01c6\7%\2\2\u01c3\u01c5\n\5\2\2\u01c4\u01c3\3")
        buf.write("\2\2\2\u01c5\u01c8\3\2\2\2\u01c6\u01c4\3\2\2\2\u01c6\u01c7")
        buf.write("\3\2\2\2\u01c7\u008c\3\2\2\2\u01c8\u01c6\3\2\2\2\u01c9")
        buf.write("\u01cb\7^\2\2\u01ca\u01cc\5\u0089E\2\u01cb\u01ca\3\2\2")
        buf.write("\2\u01cb\u01cc\3\2\2\2\u01cc\u01d2\3\2\2\2\u01cd\u01cf")
        buf.write("\7\17\2\2\u01ce\u01cd\3\2\2\2\u01ce\u01cf\3\2\2\2\u01cf")
        buf.write("\u01d0\3\2\2\2\u01d0\u01d3\7\f\2\2\u01d1\u01d3\4\16\17")
        buf.write("\2\u01d2\u01ce\3\2\2\2\u01d2\u01d1\3\2\2\2\u01d3\u008e")
        buf.write("\3\2\2\2\u01d4\u01d6\t\6\2\2\u01d5\u01d4\3\2\2\2\u01d6")
        buf.write("\u0090\3\2\2\2\u01d7\u01da\5\u008fH\2\u01d8\u01da\t\3")
        buf.write("\2\2\u01d9\u01d7\3\2\2\2\u01d9\u01d8\3\2\2\2\u01da\u0092")
        buf.write("\3\2\2\2\32\2\u014c\u0153\u015f\u0166\u016a\u016d\u016f")
        buf.write("\u0179\u017f\u0186\u018e\u0192\u0198\u019e\u01a0\u01b3")
        buf.write("\u01c0\u01c6\u01cb\u01ce\u01d2\u01d5\u01d9\4\3\65\2\b")
        buf.write("\2\2")
        return buf.getvalue()


class Python3d3Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    T__17 = 18
    T__18 = 19
    T__19 = 20
    T__20 = 21
    T__21 = 22
    T__22 = 23
    T__23 = 24
    T__24 = 25
    T__25 = 26
    T__26 = 27
    T__27 = 28
    T__28 = 29
    T__29 = 30
    T__30 = 31
    T__31 = 32
    T__32 = 33
    T__33 = 34
    T__34 = 35
    T__35 = 36
    T__36 = 37
    T__37 = 38
    T__38 = 39
    T__39 = 40
    T__40 = 41
    T__41 = 42
    T__42 = 43
    T__43 = 44
    T__44 = 45
    SEP = 46
    STRING = 47
    NUMBER = 48
    FLOAT = 49
    BOOL = 50
    INTEGER = 51
    NEWLINE = 52
    GRZLYNAME = 53
    NAME = 54
    STRING_LITERAL = 55
    DECIMAL_INTEGER = 56
    OPEN_PAREN = 57
    CLOSE_PAREN = 58
    OPEN_BRACK = 59
    CLOSE_BRACK = 60
    OPEN_BRACE = 61
    CLOSE_BRACE = 62
    ASSIGN_EQUAL = 63
    SKIP_ = 64
    UNKNOWN_CHAR = 65

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "':'", "'break'", "'continue'", "'return'", "'raise'", "'if'", 
            "'elif'", "'else'", "'while'", "'for'", "'in'", "'try:'", "'finally'", 
            "'range'", "'print'", "'and'", "'or'", "'not'", "'<'", "'>'", 
            "'=='", "'>='", "'<='", "'!='", "'+'", "'-'", "'*'", "'/'", 
            "'%'", "'**'", "'&'", "'|'", "'~'", "'^'", "'<<'", "'>>'", "'.'", 
            "'except'", "'as'", "'int'", "'str'", "'list'", "'float'", "'bool'", 
            "'None'", "','", "'('", "')'", "'['", "']'", "'{'", "'}'", "'='" ]

    symbolicNames = [ "<INVALID>",
            "SEP", "STRING", "NUMBER", "FLOAT", "BOOL", "INTEGER", "NEWLINE", 
            "GRZLYNAME", "NAME", "STRING_LITERAL", "DECIMAL_INTEGER", "OPEN_PAREN", 
            "CLOSE_PAREN", "OPEN_BRACK", "CLOSE_BRACK", "OPEN_BRACE", "CLOSE_BRACE", 
            "ASSIGN_EQUAL", "SKIP_", "UNKNOWN_CHAR" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "T__20", "T__21", "T__22", "T__23", "T__24", "T__25", 
                  "T__26", "T__27", "T__28", "T__29", "T__30", "T__31", 
                  "T__32", "T__33", "T__34", "T__35", "T__36", "T__37", 
                  "T__38", "T__39", "T__40", "T__41", "T__42", "T__43", 
                  "T__44", "SEP", "STRING", "NUMBER", "FLOAT", "BOOL", "INTEGER", 
                  "NEWLINE", "GRZLYNAME", "NAME", "STRING_LITERAL", "DECIMAL_INTEGER", 
                  "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACK", "CLOSE_BRACK", 
                  "OPEN_BRACE", "CLOSE_BRACE", "ASSIGN_EQUAL", "SKIP_", 
                  "UNKNOWN_CHAR", "NON_ZERO_DIGIT", "DIGIT", "SPACES", "COMMENT", 
                  "LINE_JOINING", "ID_START", "ID_CONTINUE" ]

    grammarFileName = "Python3d3.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    @property
    def tokens(self):
        try:
            return self._tokens
        except AttributeError:
            self._tokens = []
            return self._tokens
    @property
    def indents(self):
        try:
            return self._indents
        except AttributeError:
            self._indents = []
            return self._indents
    @property
    def opened(self):
        try:
            return self._opened
        except AttributeError:
            self._opened = 0
            return self._opened
    @opened.setter
    def opened(self, value):
        self._opened = value
    @property
    def lastToken(self):
        try:
            return self._lastToken
        except AttributeError:
            self._lastToken = None
            return self._lastToken
    @lastToken.setter
    def lastToken(self, value):
        self._lastToken = value
    def reset(self):
        super().reset()
        self.tokens = []
        self.indents = []
        self.opened = 0
        self.lastToken = None
    def emitToken(self, t):
        super().emitToken(t)
        self.tokens.append(t)
    def nextToken(self):
        if self._input.LA(1) == Token.EOF and self.indents:
            for i in range(len(self.tokens)-1,-1,-1):
                if self.tokens[i].type == Token.EOF:
                    self.tokens.pop(i)
            self.emitToken(self.commonToken(LanguageParser.NEWLINE, '\n'))
            while self.indents:
                self.emitToken(self.createDedent())
                self.indents.pop()
            self.emitToken(self.commonToken(LanguageParser.EOF, "<EOF>"))
        next = super().nextToken()
        if next.channel == Token.DEFAULT_CHANNEL:
            self.lastToken = next
        return next if not self.tokens else self.tokens.pop(0)
    def createDedent(self):
        dedent = self.commonToken(LanguageParser.DEDENT, "")
        dedent.line = self.lastToken.line
        return dedent
    def commonToken(self, type, text, indent=0):
        stop = self.getCharIndex()-1-indent
        start = (stop - len(text) + 1) if text else stop
        return CommonToken(self._tokenFactorySourcePair, type, super().DEFAULT_TOKEN_CHANNEL, start, stop)
    @staticmethod
    def getIndentationCount(spaces):
        count = 0
        for ch in spaces:
            if ch == '\t':
                count += 8 - (count % 8)
            else:
                count += 1
        return count
    def atStartOfInput(self):
        return Lexer.column.fget(self) == 0 and Lexer.line.fget(self) == 1


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[51] = self.NEWLINE_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def NEWLINE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:

            tempt = Lexer.text.fget(self)
            newLine = re.sub("[^\r\n\f]+", "", tempt)
            spaces = re.sub("[\r\n\f]+", "", tempt)
            la_char = ""
            try:
                la = self._input.LA(1)
                la_char = chr(la)       # Python does not compare char to ints directly
            except ValueError:          # End of file
                pass
            # Strip newlines inside open clauses except if we are near EOF. We keep NEWLINEs near EOF to
            # satisfy the final newline needed by the single_put rule used by the REPL.
            try:
                nextnext_la = self._input.LA(2)
                nextnext_la_char = chr(nextnext_la)
            except ValueError:
                nextnext_eof = True
            else:
                nextnext_eof = False
            if self.opened > 0 or nextnext_eof is False and (la_char == '\r' or la_char == '\n' or la_char == '\f' or la_char == '#'):
                self.skip()
            else:
                indent = self.getIndentationCount(spaces)
                previous = self.indents[-1] if self.indents else 0
                self.emitToken(self.commonToken(self.NEWLINE, newLine, indent=indent))      # NEWLINE is actually the '\n' char
                if indent == previous:
                    self.skip()
                elif indent > previous:
                    self.indents.append(indent)
                    self.emitToken(self.commonToken(LanguageParser.INDENT, spaces))
                else:
                    while self.indents and self.indents[-1] > indent:
                        self.emitToken(self.createDedent())
                        self.indents.pop()
                
     

    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates is None:
            preds = dict()
            preds[51] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 0:
                return self.atStartOfInput()
         


