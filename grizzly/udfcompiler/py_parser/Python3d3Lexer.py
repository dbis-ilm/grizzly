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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2B")
        buf.write("\u01d1\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\3\2\3\2\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\5\3\5")
        buf.write("\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3")
        buf.write("\7\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3")
        buf.write("\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16\3\17\3\17\3\17")
        buf.write("\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\21\3\21\3\21\3\22")
        buf.write("\3\22\3\22\3\22\3\23\3\23\3\24\3\24\3\25\3\25\3\25\3\26")
        buf.write("\3\26\3\26\3\27\3\27\3\27\3\30\3\30\3\30\3\31\3\31\3\32")
        buf.write("\3\32\3\33\3\33\3\34\3\34\3\35\3\35\3\36\3\36\3\36\3\37")
        buf.write("\3\37\3 \3 \3!\3!\3\"\3\"\3#\3#\3#\3$\3$\3$\3%\3%\3&\3")
        buf.write("&\3&\3&\3&\3&\3&\3\'\3\'\3\'\3(\3(\3(\3(\3)\3)\3)\3)\3")
        buf.write("*\3*\3*\3*\3*\3+\3+\3+\3+\3+\3+\3,\3,\3,\3,\3,\3-\3-\3")
        buf.write("-\3-\3-\3.\3.\3/\3/\3\60\3\60\3\61\7\61\u0141\n\61\f\61")
        buf.write("\16\61\u0144\13\61\3\61\3\61\7\61\u0148\n\61\f\61\16\61")
        buf.write("\u014b\13\61\3\62\3\62\3\62\3\62\3\62\3\62\3\62\3\62\3")
        buf.write("\62\5\62\u0156\n\62\3\63\3\63\3\64\3\64\3\64\5\64\u015d")
        buf.write("\n\64\3\64\3\64\5\64\u0161\n\64\3\64\5\64\u0164\n\64\5")
        buf.write("\64\u0166\n\64\3\64\3\64\3\65\3\65\3\65\3\65\6\65\u016e")
        buf.write("\n\65\r\65\16\65\u016f\3\66\3\66\7\66\u0174\n\66\f\66")
        buf.write("\16\66\u0177\13\66\3\67\3\67\7\67\u017b\n\67\f\67\16\67")
        buf.write("\u017e\13\67\3\67\3\67\3\67\7\67\u0183\n\67\f\67\16\67")
        buf.write("\u0186\13\67\3\67\5\67\u0189\n\67\38\38\78\u018d\n8\f")
        buf.write("8\168\u0190\138\38\68\u0193\n8\r8\168\u0194\58\u0197\n")
        buf.write("8\39\39\3:\3:\3;\3;\3<\3<\3=\3=\3>\3>\3?\3?\3@\3@\3@\5")
        buf.write("@\u01aa\n@\3@\3@\3A\3A\3B\3B\3C\3C\3D\6D\u01b5\nD\rD\16")
        buf.write("D\u01b6\3E\3E\7E\u01bb\nE\fE\16E\u01be\13E\3F\3F\5F\u01c2")
        buf.write("\nF\3F\5F\u01c5\nF\3F\3F\5F\u01c9\nF\3G\5G\u01cc\nG\3")
        buf.write("H\3H\5H\u01d0\nH\4\u017c\u0184\2I\3\3\5\4\7\5\t\6\13\7")
        buf.write("\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21")
        buf.write("!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67")
        buf.write("\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61")
        buf.write("a\62c\63e\64g\65i\66k\67m8o9q:s;u<w=y>{?}@\177A\u0081")
        buf.write("B\u0083\2\u0085\2\u0087\2\u0089\2\u008b\2\u008d\2\u008f")
        buf.write("\2\3\2\7\3\2\63;\3\2\62;\4\2\13\13\"\"\4\2\f\f\16\17\5")
        buf.write("\2C\\aac|\2\u01e0\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2")
        buf.write("\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21")
        buf.write("\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3")
        buf.write("\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2")
        buf.write("\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2")
        buf.write("\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2")
        buf.write("\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2")
        buf.write("\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3")
        buf.write("\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q")
        buf.write("\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2")
        buf.write("[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2")
        buf.write("\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2")
        buf.write("\2\2o\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2")
        buf.write("\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2")
        buf.write("\u0081\3\2\2\2\3\u0091\3\2\2\2\5\u0093\3\2\2\2\7\u0099")
        buf.write("\3\2\2\2\t\u00a2\3\2\2\2\13\u00a9\3\2\2\2\r\u00af\3\2")
        buf.write("\2\2\17\u00b2\3\2\2\2\21\u00b7\3\2\2\2\23\u00bc\3\2\2")
        buf.write("\2\25\u00c2\3\2\2\2\27\u00c6\3\2\2\2\31\u00c9\3\2\2\2")
        buf.write("\33\u00ce\3\2\2\2\35\u00d4\3\2\2\2\37\u00da\3\2\2\2!\u00de")
        buf.write("\3\2\2\2#\u00e1\3\2\2\2%\u00e5\3\2\2\2\'\u00e7\3\2\2\2")
        buf.write(")\u00e9\3\2\2\2+\u00ec\3\2\2\2-\u00ef\3\2\2\2/\u00f2\3")
        buf.write("\2\2\2\61\u00f5\3\2\2\2\63\u00f7\3\2\2\2\65\u00f9\3\2")
        buf.write("\2\2\67\u00fb\3\2\2\29\u00fd\3\2\2\2;\u00ff\3\2\2\2=\u0102")
        buf.write("\3\2\2\2?\u0104\3\2\2\2A\u0106\3\2\2\2C\u0108\3\2\2\2")
        buf.write("E\u010a\3\2\2\2G\u010d\3\2\2\2I\u0110\3\2\2\2K\u0112\3")
        buf.write("\2\2\2M\u0119\3\2\2\2O\u011c\3\2\2\2Q\u0120\3\2\2\2S\u0124")
        buf.write("\3\2\2\2U\u0129\3\2\2\2W\u012f\3\2\2\2Y\u0134\3\2\2\2")
        buf.write("[\u0139\3\2\2\2]\u013b\3\2\2\2_\u013d\3\2\2\2a\u0142\3")
        buf.write("\2\2\2c\u0155\3\2\2\2e\u0157\3\2\2\2g\u0165\3\2\2\2i\u0169")
        buf.write("\3\2\2\2k\u0171\3\2\2\2m\u0188\3\2\2\2o\u0196\3\2\2\2")
        buf.write("q\u0198\3\2\2\2s\u019a\3\2\2\2u\u019c\3\2\2\2w\u019e\3")
        buf.write("\2\2\2y\u01a0\3\2\2\2{\u01a2\3\2\2\2}\u01a4\3\2\2\2\177")
        buf.write("\u01a9\3\2\2\2\u0081\u01ad\3\2\2\2\u0083\u01af\3\2\2\2")
        buf.write("\u0085\u01b1\3\2\2\2\u0087\u01b4\3\2\2\2\u0089\u01b8\3")
        buf.write("\2\2\2\u008b\u01bf\3\2\2\2\u008d\u01cb\3\2\2\2\u008f\u01cf")
        buf.write("\3\2\2\2\u0091\u0092\7<\2\2\u0092\4\3\2\2\2\u0093\u0094")
        buf.write("\7d\2\2\u0094\u0095\7t\2\2\u0095\u0096\7g\2\2\u0096\u0097")
        buf.write("\7c\2\2\u0097\u0098\7m\2\2\u0098\6\3\2\2\2\u0099\u009a")
        buf.write("\7e\2\2\u009a\u009b\7q\2\2\u009b\u009c\7p\2\2\u009c\u009d")
        buf.write("\7v\2\2\u009d\u009e\7k\2\2\u009e\u009f\7p\2\2\u009f\u00a0")
        buf.write("\7w\2\2\u00a0\u00a1\7g\2\2\u00a1\b\3\2\2\2\u00a2\u00a3")
        buf.write("\7t\2\2\u00a3\u00a4\7g\2\2\u00a4\u00a5\7v\2\2\u00a5\u00a6")
        buf.write("\7w\2\2\u00a6\u00a7\7t\2\2\u00a7\u00a8\7p\2\2\u00a8\n")
        buf.write("\3\2\2\2\u00a9\u00aa\7t\2\2\u00aa\u00ab\7c\2\2\u00ab\u00ac")
        buf.write("\7k\2\2\u00ac\u00ad\7u\2\2\u00ad\u00ae\7g\2\2\u00ae\f")
        buf.write("\3\2\2\2\u00af\u00b0\7k\2\2\u00b0\u00b1\7h\2\2\u00b1\16")
        buf.write("\3\2\2\2\u00b2\u00b3\7g\2\2\u00b3\u00b4\7n\2\2\u00b4\u00b5")
        buf.write("\7k\2\2\u00b5\u00b6\7h\2\2\u00b6\20\3\2\2\2\u00b7\u00b8")
        buf.write("\7g\2\2\u00b8\u00b9\7n\2\2\u00b9\u00ba\7u\2\2\u00ba\u00bb")
        buf.write("\7g\2\2\u00bb\22\3\2\2\2\u00bc\u00bd\7y\2\2\u00bd\u00be")
        buf.write("\7j\2\2\u00be\u00bf\7k\2\2\u00bf\u00c0\7n\2\2\u00c0\u00c1")
        buf.write("\7g\2\2\u00c1\24\3\2\2\2\u00c2\u00c3\7h\2\2\u00c3\u00c4")
        buf.write("\7q\2\2\u00c4\u00c5\7t\2\2\u00c5\26\3\2\2\2\u00c6\u00c7")
        buf.write("\7k\2\2\u00c7\u00c8\7p\2\2\u00c8\30\3\2\2\2\u00c9\u00ca")
        buf.write("\7v\2\2\u00ca\u00cb\7t\2\2\u00cb\u00cc\7{\2\2\u00cc\u00cd")
        buf.write("\7<\2\2\u00cd\32\3\2\2\2\u00ce\u00cf\7t\2\2\u00cf\u00d0")
        buf.write("\7c\2\2\u00d0\u00d1\7p\2\2\u00d1\u00d2\7i\2\2\u00d2\u00d3")
        buf.write("\7g\2\2\u00d3\34\3\2\2\2\u00d4\u00d5\7r\2\2\u00d5\u00d6")
        buf.write("\7t\2\2\u00d6\u00d7\7k\2\2\u00d7\u00d8\7p\2\2\u00d8\u00d9")
        buf.write("\7v\2\2\u00d9\36\3\2\2\2\u00da\u00db\7c\2\2\u00db\u00dc")
        buf.write("\7p\2\2\u00dc\u00dd\7f\2\2\u00dd \3\2\2\2\u00de\u00df")
        buf.write("\7q\2\2\u00df\u00e0\7t\2\2\u00e0\"\3\2\2\2\u00e1\u00e2")
        buf.write("\7p\2\2\u00e2\u00e3\7q\2\2\u00e3\u00e4\7v\2\2\u00e4$\3")
        buf.write("\2\2\2\u00e5\u00e6\7>\2\2\u00e6&\3\2\2\2\u00e7\u00e8\7")
        buf.write("@\2\2\u00e8(\3\2\2\2\u00e9\u00ea\7?\2\2\u00ea\u00eb\7")
        buf.write("?\2\2\u00eb*\3\2\2\2\u00ec\u00ed\7@\2\2\u00ed\u00ee\7")
        buf.write("?\2\2\u00ee,\3\2\2\2\u00ef\u00f0\7>\2\2\u00f0\u00f1\7")
        buf.write("?\2\2\u00f1.\3\2\2\2\u00f2\u00f3\7#\2\2\u00f3\u00f4\7")
        buf.write("?\2\2\u00f4\60\3\2\2\2\u00f5\u00f6\7-\2\2\u00f6\62\3\2")
        buf.write("\2\2\u00f7\u00f8\7/\2\2\u00f8\64\3\2\2\2\u00f9\u00fa\7")
        buf.write(",\2\2\u00fa\66\3\2\2\2\u00fb\u00fc\7\61\2\2\u00fc8\3\2")
        buf.write("\2\2\u00fd\u00fe\7\'\2\2\u00fe:\3\2\2\2\u00ff\u0100\7")
        buf.write(",\2\2\u0100\u0101\7,\2\2\u0101<\3\2\2\2\u0102\u0103\7")
        buf.write("(\2\2\u0103>\3\2\2\2\u0104\u0105\7~\2\2\u0105@\3\2\2\2")
        buf.write("\u0106\u0107\7\u0080\2\2\u0107B\3\2\2\2\u0108\u0109\7")
        buf.write("`\2\2\u0109D\3\2\2\2\u010a\u010b\7>\2\2\u010b\u010c\7")
        buf.write(">\2\2\u010cF\3\2\2\2\u010d\u010e\7@\2\2\u010e\u010f\7")
        buf.write("@\2\2\u010fH\3\2\2\2\u0110\u0111\7\60\2\2\u0111J\3\2\2")
        buf.write("\2\u0112\u0113\7g\2\2\u0113\u0114\7z\2\2\u0114\u0115\7")
        buf.write("e\2\2\u0115\u0116\7g\2\2\u0116\u0117\7r\2\2\u0117\u0118")
        buf.write("\7v\2\2\u0118L\3\2\2\2\u0119\u011a\7c\2\2\u011a\u011b")
        buf.write("\7u\2\2\u011bN\3\2\2\2\u011c\u011d\7k\2\2\u011d\u011e")
        buf.write("\7p\2\2\u011e\u011f\7v\2\2\u011fP\3\2\2\2\u0120\u0121")
        buf.write("\7u\2\2\u0121\u0122\7v\2\2\u0122\u0123\7t\2\2\u0123R\3")
        buf.write("\2\2\2\u0124\u0125\7n\2\2\u0125\u0126\7k\2\2\u0126\u0127")
        buf.write("\7u\2\2\u0127\u0128\7v\2\2\u0128T\3\2\2\2\u0129\u012a")
        buf.write("\7h\2\2\u012a\u012b\7n\2\2\u012b\u012c\7q\2\2\u012c\u012d")
        buf.write("\7c\2\2\u012d\u012e\7v\2\2\u012eV\3\2\2\2\u012f\u0130")
        buf.write("\7d\2\2\u0130\u0131\7q\2\2\u0131\u0132\7q\2\2\u0132\u0133")
        buf.write("\7n\2\2\u0133X\3\2\2\2\u0134\u0135\7P\2\2\u0135\u0136")
        buf.write("\7q\2\2\u0136\u0137\7p\2\2\u0137\u0138\7g\2\2\u0138Z\3")
        buf.write("\2\2\2\u0139\u013a\7.\2\2\u013a\\\3\2\2\2\u013b\u013c")
        buf.write("\5m\67\2\u013c^\3\2\2\2\u013d\u013e\5e\63\2\u013e`\3\2")
        buf.write("\2\2\u013f\u0141\5\u0085C\2\u0140\u013f\3\2\2\2\u0141")
        buf.write("\u0144\3\2\2\2\u0142\u0140\3\2\2\2\u0142\u0143\3\2\2\2")
        buf.write("\u0143\u0145\3\2\2\2\u0144\u0142\3\2\2\2\u0145\u0149\7")
        buf.write("\60\2\2\u0146\u0148\5\u0085C\2\u0147\u0146\3\2\2\2\u0148")
        buf.write("\u014b\3\2\2\2\u0149\u0147\3\2\2\2\u0149\u014a\3\2\2\2")
        buf.write("\u014ab\3\2\2\2\u014b\u0149\3\2\2\2\u014c\u014d\7V\2\2")
        buf.write("\u014d\u014e\7t\2\2\u014e\u014f\7w\2\2\u014f\u0156\7g")
        buf.write("\2\2\u0150\u0151\7H\2\2\u0151\u0152\7c\2\2\u0152\u0153")
        buf.write("\7n\2\2\u0153\u0154\7u\2\2\u0154\u0156\7g\2\2\u0155\u014c")
        buf.write("\3\2\2\2\u0155\u0150\3\2\2\2\u0156d\3\2\2\2\u0157\u0158")
        buf.write("\5o8\2\u0158f\3\2\2\2\u0159\u015a\6\64\2\2\u015a\u0166")
        buf.write("\5\u0087D\2\u015b\u015d\7\17\2\2\u015c\u015b\3\2\2\2\u015c")
        buf.write("\u015d\3\2\2\2\u015d\u015e\3\2\2\2\u015e\u0161\7\f\2\2")
        buf.write("\u015f\u0161\4\16\17\2\u0160\u015c\3\2\2\2\u0160\u015f")
        buf.write("\3\2\2\2\u0161\u0163\3\2\2\2\u0162\u0164\5\u0087D\2\u0163")
        buf.write("\u0162\3\2\2\2\u0163\u0164\3\2\2\2\u0164\u0166\3\2\2\2")
        buf.write("\u0165\u0159\3\2\2\2\u0165\u0160\3\2\2\2\u0166\u0167\3")
        buf.write("\2\2\2\u0167\u0168\b\64\2\2\u0168h\3\2\2\2\u0169\u016a")
        buf.write("\7i\2\2\u016a\u016b\7a\2\2\u016b\u016d\3\2\2\2\u016c\u016e")
        buf.write("\5\u008fH\2\u016d\u016c\3\2\2\2\u016e\u016f\3\2\2\2\u016f")
        buf.write("\u016d\3\2\2\2\u016f\u0170\3\2\2\2\u0170j\3\2\2\2\u0171")
        buf.write("\u0175\5\u008dG\2\u0172\u0174\5\u008fH\2\u0173\u0172\3")
        buf.write("\2\2\2\u0174\u0177\3\2\2\2\u0175\u0173\3\2\2\2\u0175\u0176")
        buf.write("\3\2\2\2\u0176l\3\2\2\2\u0177\u0175\3\2\2\2\u0178\u017c")
        buf.write("\7$\2\2\u0179\u017b\13\2\2\2\u017a\u0179\3\2\2\2\u017b")
        buf.write("\u017e\3\2\2\2\u017c\u017d\3\2\2\2\u017c\u017a\3\2\2\2")
        buf.write("\u017d\u017f\3\2\2\2\u017e\u017c\3\2\2\2\u017f\u0189\7")
        buf.write("$\2\2\u0180\u0184\7)\2\2\u0181\u0183\13\2\2\2\u0182\u0181")
        buf.write("\3\2\2\2\u0183\u0186\3\2\2\2\u0184\u0185\3\2\2\2\u0184")
        buf.write("\u0182\3\2\2\2\u0185\u0187\3\2\2\2\u0186\u0184\3\2\2\2")
        buf.write("\u0187\u0189\7)\2\2\u0188\u0178\3\2\2\2\u0188\u0180\3")
        buf.write("\2\2\2\u0189n\3\2\2\2\u018a\u018e\5\u0083B\2\u018b\u018d")
        buf.write("\5\u0085C\2\u018c\u018b\3\2\2\2\u018d\u0190\3\2\2\2\u018e")
        buf.write("\u018c\3\2\2\2\u018e\u018f\3\2\2\2\u018f\u0197\3\2\2\2")
        buf.write("\u0190\u018e\3\2\2\2\u0191\u0193\7\62\2\2\u0192\u0191")
        buf.write("\3\2\2\2\u0193\u0194\3\2\2\2\u0194\u0192\3\2\2\2\u0194")
        buf.write("\u0195\3\2\2\2\u0195\u0197\3\2\2\2\u0196\u018a\3\2\2\2")
        buf.write("\u0196\u0192\3\2\2\2\u0197p\3\2\2\2\u0198\u0199\7*\2\2")
        buf.write("\u0199r\3\2\2\2\u019a\u019b\7+\2\2\u019bt\3\2\2\2\u019c")
        buf.write("\u019d\7]\2\2\u019dv\3\2\2\2\u019e\u019f\7_\2\2\u019f")
        buf.write("x\3\2\2\2\u01a0\u01a1\7}\2\2\u01a1z\3\2\2\2\u01a2\u01a3")
        buf.write("\7\177\2\2\u01a3|\3\2\2\2\u01a4\u01a5\7?\2\2\u01a5~\3")
        buf.write("\2\2\2\u01a6\u01aa\5\u0087D\2\u01a7\u01aa\5\u0089E\2\u01a8")
        buf.write("\u01aa\5\u008bF\2\u01a9\u01a6\3\2\2\2\u01a9\u01a7\3\2")
        buf.write("\2\2\u01a9\u01a8\3\2\2\2\u01aa\u01ab\3\2\2\2\u01ab\u01ac")
        buf.write("\b@\3\2\u01ac\u0080\3\2\2\2\u01ad\u01ae\13\2\2\2\u01ae")
        buf.write("\u0082\3\2\2\2\u01af\u01b0\t\2\2\2\u01b0\u0084\3\2\2\2")
        buf.write("\u01b1\u01b2\t\3\2\2\u01b2\u0086\3\2\2\2\u01b3\u01b5\t")
        buf.write("\4\2\2\u01b4\u01b3\3\2\2\2\u01b5\u01b6\3\2\2\2\u01b6\u01b4")
        buf.write("\3\2\2\2\u01b6\u01b7\3\2\2\2\u01b7\u0088\3\2\2\2\u01b8")
        buf.write("\u01bc\7%\2\2\u01b9\u01bb\n\5\2\2\u01ba\u01b9\3\2\2\2")
        buf.write("\u01bb\u01be\3\2\2\2\u01bc\u01ba\3\2\2\2\u01bc\u01bd\3")
        buf.write("\2\2\2\u01bd\u008a\3\2\2\2\u01be\u01bc\3\2\2\2\u01bf\u01c1")
        buf.write("\7^\2\2\u01c0\u01c2\5\u0087D\2\u01c1\u01c0\3\2\2\2\u01c1")
        buf.write("\u01c2\3\2\2\2\u01c2\u01c8\3\2\2\2\u01c3\u01c5\7\17\2")
        buf.write("\2\u01c4\u01c3\3\2\2\2\u01c4\u01c5\3\2\2\2\u01c5\u01c6")
        buf.write("\3\2\2\2\u01c6\u01c9\7\f\2\2\u01c7\u01c9\4\16\17\2\u01c8")
        buf.write("\u01c4\3\2\2\2\u01c8\u01c7\3\2\2\2\u01c9\u008c\3\2\2\2")
        buf.write("\u01ca\u01cc\t\6\2\2\u01cb\u01ca\3\2\2\2\u01cc\u008e\3")
        buf.write("\2\2\2\u01cd\u01d0\5\u008dG\2\u01ce\u01d0\t\3\2\2\u01cf")
        buf.write("\u01cd\3\2\2\2\u01cf\u01ce\3\2\2\2\u01d0\u0090\3\2\2\2")
        buf.write("\32\2\u0142\u0149\u0155\u015c\u0160\u0163\u0165\u016f")
        buf.write("\u0175\u017c\u0184\u0188\u018e\u0194\u0196\u01a9\u01b6")
        buf.write("\u01bc\u01c1\u01c4\u01c8\u01cb\u01cf\4\3\64\2\b\2\2")
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
    SEP = 45
    STRING = 46
    NUMBER = 47
    FLOAT = 48
    BOOL = 49
    INTEGER = 50
    NEWLINE = 51
    GRZLYNAME = 52
    NAME = 53
    STRING_LITERAL = 54
    DECIMAL_INTEGER = 55
    OPEN_PAREN = 56
    CLOSE_PAREN = 57
    OPEN_BRACK = 58
    CLOSE_BRACK = 59
    OPEN_BRACE = 60
    CLOSE_BRACE = 61
    ASSIGN_EQUAL = 62
    SKIP_ = 63
    UNKNOWN_CHAR = 64

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "':'", "'break'", "'continue'", "'return'", "'raise'", "'if'", 
            "'elif'", "'else'", "'while'", "'for'", "'in'", "'try:'", "'range'", 
            "'print'", "'and'", "'or'", "'not'", "'<'", "'>'", "'=='", "'>='", 
            "'<='", "'!='", "'+'", "'-'", "'*'", "'/'", "'%'", "'**'", "'&'", 
            "'|'", "'~'", "'^'", "'<<'", "'>>'", "'.'", "'except'", "'as'", 
            "'int'", "'str'", "'list'", "'float'", "'bool'", "'None'", "','", 
            "'('", "')'", "'['", "']'", "'{'", "'}'", "'='" ]

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
                  "SEP", "STRING", "NUMBER", "FLOAT", "BOOL", "INTEGER", 
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
            actions[50] = self.NEWLINE_action 
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
            preds[50] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 0:
                return self.atStartOfInput()
         


