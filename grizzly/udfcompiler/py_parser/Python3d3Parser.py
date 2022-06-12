# Generated from grammar/Python3d3.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3D")
        buf.write("\u01a6\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36")
        buf.write("\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t")
        buf.write("&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\3\2\3\2\7\2Y\n\2\f\2")
        buf.write("\16\2\\\13\2\3\2\3\2\3\3\3\3\5\3b\n\3\3\4\3\4\3\4\3\5")
        buf.write("\3\5\3\5\3\5\3\5\5\5l\n\5\3\6\3\6\3\6\3\6\5\6r\n\6\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3")
        buf.write("\t\3\t\5\t\u0084\n\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\13")
        buf.write("\3\13\3\13\3\13\5\13\u0091\n\13\3\f\3\f\3\r\3\r\3\16\3")
        buf.write("\16\3\16\3\17\3\17\5\17\u009c\n\17\3\20\3\20\3\20\3\20")
        buf.write("\5\20\u00a2\n\20\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3")
        buf.write("\21\3\21\7\21\u00ad\n\21\f\21\16\21\u00b0\13\21\3\21\3")
        buf.write("\21\3\21\5\21\u00b5\n\21\3\22\3\22\3\22\3\22\3\22\3\23")
        buf.write("\3\23\3\23\3\23\3\23\3\23\5\23\u00c2\n\23\3\23\3\23\3")
        buf.write("\23\3\24\3\24\3\24\3\24\3\24\3\24\7\24\u00cd\n\24\f\24")
        buf.write("\16\24\u00d0\13\24\3\25\3\25\3\25\3\25\6\25\u00d6\n\25")
        buf.write("\r\25\16\25\u00d7\3\25\3\25\5\25\u00dc\n\25\3\26\3\26")
        buf.write("\3\26\3\26\3\26\5\26\u00e3\n\26\3\26\3\26\3\27\3\27\3")
        buf.write("\27\3\27\7\27\u00eb\n\27\f\27\16\27\u00ee\13\27\3\30\3")
        buf.write("\30\3\30\3\30\7\30\u00f4\n\30\f\30\16\30\u00f7\13\30\3")
        buf.write("\31\3\31\3\31\3\31\3\31\3\32\3\32\3\33\3\33\3\34\3\34")
        buf.write("\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\5\35\u0110\n\35\3\35\3\35\3\35\3\35\7\35\u0116\n")
        buf.write("\35\f\35\16\35\u0119\13\35\3\36\3\36\3\36\3\36\3\36\3")
        buf.write("\36\3\36\3\36\3\36\3\36\7\36\u0125\n\36\f\36\16\36\u0128")
        buf.write("\13\36\3\36\3\36\3\36\5\36\u012d\n\36\3\36\3\36\3\36\3")
        buf.write("\36\3\36\3\36\7\36\u0135\n\36\f\36\16\36\u0138\13\36\3")
        buf.write("\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\5\36\u0158\n")
        buf.write("\36\3\37\3\37\3\37\3\37\3\37\3 \3 \5 \u0161\n \3 \3 \3")
        buf.write("!\3!\3!\7!\u0168\n!\f!\16!\u016b\13!\3\"\3\"\3#\3#\3#")
        buf.write("\3#\3$\3$\3$\3$\3%\3%\5%\u0179\n%\3%\3%\3%\3%\3%\3&\3")
        buf.write("&\3&\3&\3&\3\'\3\'\3\'\7\'\u0188\n\'\f\'\16\'\u018b\13")
        buf.write("\'\7\'\u018d\n\'\f\'\16\'\u0190\13\'\3(\3(\6(\u0194\n")
        buf.write("(\r(\16(\u0195\3)\3)\5)\u019a\n)\3)\3)\5)\u019e\n)\3*")
        buf.write("\3*\3+\3+\3+\3+\3+\2\38,\2\4\6\b\n\f\16\20\22\24\26\30")
        buf.write("\32\34\36 \"$&(*,.\60\62\64\668:<>@BDFHJLNPRT\2\7\3\2")
        buf.write("\21\23\3\2\24\31\3\2\32%\4\2\60\63\67\67\3\2).\2\u01b8")
        buf.write("\2Z\3\2\2\2\4a\3\2\2\2\6c\3\2\2\2\bk\3\2\2\2\nq\3\2\2")
        buf.write("\2\fs\3\2\2\2\16y\3\2\2\2\20\u0083\3\2\2\2\22\u0085\3")
        buf.write("\2\2\2\24\u0090\3\2\2\2\26\u0092\3\2\2\2\30\u0094\3\2")
        buf.write("\2\2\32\u0096\3\2\2\2\34\u0099\3\2\2\2\36\u00a1\3\2\2")
        buf.write("\2 \u00a3\3\2\2\2\"\u00b6\3\2\2\2$\u00bb\3\2\2\2&\u00c6")
        buf.write("\3\2\2\2(\u00db\3\2\2\2*\u00dd\3\2\2\2,\u00e6\3\2\2\2")
        buf.write(".\u00ef\3\2\2\2\60\u00f8\3\2\2\2\62\u00fd\3\2\2\2\64\u00ff")
        buf.write("\3\2\2\2\66\u0101\3\2\2\28\u010f\3\2\2\2:\u0157\3\2\2")
        buf.write("\2<\u0159\3\2\2\2>\u015e\3\2\2\2@\u0164\3\2\2\2B\u016c")
        buf.write("\3\2\2\2D\u016e\3\2\2\2F\u0172\3\2\2\2H\u0178\3\2\2\2")
        buf.write("J\u017f\3\2\2\2L\u018e\3\2\2\2N\u0191\3\2\2\2P\u0197\3")
        buf.write("\2\2\2R\u019f\3\2\2\2T\u01a1\3\2\2\2VY\7\65\2\2WY\5\4")
        buf.write("\3\2XV\3\2\2\2XW\3\2\2\2Y\\\3\2\2\2ZX\3\2\2\2Z[\3\2\2")
        buf.write("\2[]\3\2\2\2\\Z\3\2\2\2]^\7\2\2\3^\3\3\2\2\2_b\5\6\4\2")
        buf.write("`b\5\36\20\2a_\3\2\2\2a`\3\2\2\2b\5\3\2\2\2cd\5\b\5\2")
        buf.write("de\7\65\2\2e\7\3\2\2\2fl\5\n\6\2gl\5\24\13\2hl\5\60\31")
        buf.write("\2il\5H%\2jl\5N(\2kf\3\2\2\2kg\3\2\2\2kh\3\2\2\2ki\3\2")
        buf.write("\2\2kj\3\2\2\2l\t\3\2\2\2mr\5\f\7\2nr\5\16\b\2or\5\20")
        buf.write("\t\2pr\5\22\n\2qm\3\2\2\2qn\3\2\2\2qo\3\2\2\2qp\3\2\2")
        buf.write("\2r\13\3\2\2\2st\7\67\2\2tu\7\3\2\2uv\5R*\2vw\7@\2\2w")
        buf.write("x\58\35\2x\r\3\2\2\2yz\7\67\2\2z{\7\3\2\2{|\5R*\2|\17")
        buf.write("\3\2\2\2}~\7\66\2\2~\177\7@\2\2\177\u0084\5:\36\2\u0080")
        buf.write("\u0081\7\67\2\2\u0081\u0082\7@\2\2\u0082\u0084\58\35\2")
        buf.write("\u0083}\3\2\2\2\u0083\u0080\3\2\2\2\u0084\21\3\2\2\2\u0085")
        buf.write("\u0086\7\67\2\2\u0086\u0087\7<\2\2\u0087\u0088\7\61\2")
        buf.write("\2\u0088\u0089\7=\2\2\u0089\u008a\7@\2\2\u008a\u008b\5")
        buf.write("8\35\2\u008b\23\3\2\2\2\u008c\u0091\5\26\f\2\u008d\u0091")
        buf.write("\5\30\r\2\u008e\u0091\5\32\16\2\u008f\u0091\5\34\17\2")
        buf.write("\u0090\u008c\3\2\2\2\u0090\u008d\3\2\2\2\u0090\u008e\3")
        buf.write("\2\2\2\u0090\u008f\3\2\2\2\u0091\25\3\2\2\2\u0092\u0093")
        buf.write("\7\4\2\2\u0093\27\3\2\2\2\u0094\u0095\7\5\2\2\u0095\31")
        buf.write("\3\2\2\2\u0096\u0097\7\6\2\2\u0097\u0098\58\35\2\u0098")
        buf.write("\33\3\2\2\2\u0099\u009b\7\7\2\2\u009a\u009c\7\67\2\2\u009b")
        buf.write("\u009a\3\2\2\2\u009b\u009c\3\2\2\2\u009c\35\3\2\2\2\u009d")
        buf.write("\u00a2\5 \21\2\u009e\u00a2\5\"\22\2\u009f\u00a2\5$\23")
        buf.write("\2\u00a0\u00a2\5&\24\2\u00a1\u009d\3\2\2\2\u00a1\u009e")
        buf.write("\3\2\2\2\u00a1\u009f\3\2\2\2\u00a1\u00a0\3\2\2\2\u00a2")
        buf.write("\37\3\2\2\2\u00a3\u00a4\7\b\2\2\u00a4\u00a5\5,\27\2\u00a5")
        buf.write("\u00a6\7\3\2\2\u00a6\u00ae\5(\25\2\u00a7\u00a8\7\t\2\2")
        buf.write("\u00a8\u00a9\5,\27\2\u00a9\u00aa\7\3\2\2\u00aa\u00ab\5")
        buf.write("(\25\2\u00ab\u00ad\3\2\2\2\u00ac\u00a7\3\2\2\2\u00ad\u00b0")
        buf.write("\3\2\2\2\u00ae\u00ac\3\2\2\2\u00ae\u00af\3\2\2\2\u00af")
        buf.write("\u00b4\3\2\2\2\u00b0\u00ae\3\2\2\2\u00b1\u00b2\7\n\2\2")
        buf.write("\u00b2\u00b3\7\3\2\2\u00b3\u00b5\5(\25\2\u00b4\u00b1\3")
        buf.write("\2\2\2\u00b4\u00b5\3\2\2\2\u00b5!\3\2\2\2\u00b6\u00b7")
        buf.write("\7\13\2\2\u00b7\u00b8\5,\27\2\u00b8\u00b9\7\3\2\2\u00b9")
        buf.write("\u00ba\5(\25\2\u00ba#\3\2\2\2\u00bb\u00bc\7\f\2\2\u00bc")
        buf.write("\u00bd\7\67\2\2\u00bd\u00c1\7\r\2\2\u00be\u00c2\58\35")
        buf.write("\2\u00bf\u00c2\5*\26\2\u00c0\u00c2\7\66\2\2\u00c1\u00be")
        buf.write("\3\2\2\2\u00c1\u00bf\3\2\2\2\u00c1\u00c0\3\2\2\2\u00c2")
        buf.write("\u00c3\3\2\2\2\u00c3\u00c4\7\3\2\2\u00c4\u00c5\5(\25\2")
        buf.write("\u00c5%\3\2\2\2\u00c6\u00c7\7\16\2\2\u00c7\u00ce\5(\25")
        buf.write("\2\u00c8\u00c9\5P)\2\u00c9\u00ca\7\3\2\2\u00ca\u00cb\5")
        buf.write("(\25\2\u00cb\u00cd\3\2\2\2\u00cc\u00c8\3\2\2\2\u00cd\u00d0")
        buf.write("\3\2\2\2\u00ce\u00cc\3\2\2\2\u00ce\u00cf\3\2\2\2\u00cf")
        buf.write("\'\3\2\2\2\u00d0\u00ce\3\2\2\2\u00d1\u00dc\5\6\4\2\u00d2")
        buf.write("\u00d3\7\65\2\2\u00d3\u00d5\7C\2\2\u00d4\u00d6\5\4\3\2")
        buf.write("\u00d5\u00d4\3\2\2\2\u00d6\u00d7\3\2\2\2\u00d7\u00d5\3")
        buf.write("\2\2\2\u00d7\u00d8\3\2\2\2\u00d8\u00d9\3\2\2\2\u00d9\u00da")
        buf.write("\7D\2\2\u00da\u00dc\3\2\2\2\u00db\u00d1\3\2\2\2\u00db")
        buf.write("\u00d2\3\2\2\2\u00dc)\3\2\2\2\u00dd\u00de\7\17\2\2\u00de")
        buf.write("\u00df\7:\2\2\u00df\u00e2\58\35\2\u00e0\u00e1\7/\2\2\u00e1")
        buf.write("\u00e3\58\35\2\u00e2\u00e0\3\2\2\2\u00e2\u00e3\3\2\2\2")
        buf.write("\u00e3\u00e4\3\2\2\2\u00e4\u00e5\7;\2\2\u00e5+\3\2\2\2")
        buf.write("\u00e6\u00ec\5.\30\2\u00e7\u00e8\5\62\32\2\u00e8\u00e9")
        buf.write("\5.\30\2\u00e9\u00eb\3\2\2\2\u00ea\u00e7\3\2\2\2\u00eb")
        buf.write("\u00ee\3\2\2\2\u00ec\u00ea\3\2\2\2\u00ec\u00ed\3\2\2\2")
        buf.write("\u00ed-\3\2\2\2\u00ee\u00ec\3\2\2\2\u00ef\u00f5\58\35")
        buf.write("\2\u00f0\u00f1\5\64\33\2\u00f1\u00f2\58\35\2\u00f2\u00f4")
        buf.write("\3\2\2\2\u00f3\u00f0\3\2\2\2\u00f4\u00f7\3\2\2\2\u00f5")
        buf.write("\u00f3\3\2\2\2\u00f5\u00f6\3\2\2\2\u00f6/\3\2\2\2\u00f7")
        buf.write("\u00f5\3\2\2\2\u00f8\u00f9\7\20\2\2\u00f9\u00fa\7:\2\2")
        buf.write("\u00fa\u00fb\58\35\2\u00fb\u00fc\7;\2\2\u00fc\61\3\2\2")
        buf.write("\2\u00fd\u00fe\t\2\2\2\u00fe\63\3\2\2\2\u00ff\u0100\t")
        buf.write("\3\2\2\u0100\65\3\2\2\2\u0101\u0102\t\4\2\2\u0102\67\3")
        buf.write("\2\2\2\u0103\u0104\b\35\1\2\u0104\u0110\7\67\2\2\u0105")
        buf.write("\u0110\7\60\2\2\u0106\u0110\7\62\2\2\u0107\u0110\7\61")
        buf.write("\2\2\u0108\u0110\7\63\2\2\u0109\u0110\5> \2\u010a\u0110")
        buf.write("\5<\37\2\u010b\u0110\5T+\2\u010c\u0110\5J&\2\u010d\u0110")
        buf.write("\5D#\2\u010e\u0110\5H%\2\u010f\u0103\3\2\2\2\u010f\u0105")
        buf.write("\3\2\2\2\u010f\u0106\3\2\2\2\u010f\u0107\3\2\2\2\u010f")
        buf.write("\u0108\3\2\2\2\u010f\u0109\3\2\2\2\u010f\u010a\3\2\2\2")
        buf.write("\u010f\u010b\3\2\2\2\u010f\u010c\3\2\2\2\u010f\u010d\3")
        buf.write("\2\2\2\u010f\u010e\3\2\2\2\u0110\u0117\3\2\2\2\u0111\u0112")
        buf.write("\f\16\2\2\u0112\u0113\5\66\34\2\u0113\u0114\58\35\17\u0114")
        buf.write("\u0116\3\2\2\2\u0115\u0111\3\2\2\2\u0116\u0119\3\2\2\2")
        buf.write("\u0117\u0115\3\2\2\2\u0117\u0118\3\2\2\2\u01189\3\2\2")
        buf.write("\2\u0119\u0117\3\2\2\2\u011a\u011b\7\66\2\2\u011b\u0158")
        buf.write("\58\35\2\u011c\u011d\7\66\2\2\u011d\u0126\7<\2\2\u011e")
        buf.write("\u011f\7\66\2\2\u011f\u0120\7&\2\2\u0120\u0121\7\67\2")
        buf.write("\2\u0121\u0122\5\64\33\2\u0122\u0123\58\35\2\u0123\u0125")
        buf.write("\3\2\2\2\u0124\u011e\3\2\2\2\u0125\u0128\3\2\2\2\u0126")
        buf.write("\u0124\3\2\2\2\u0126\u0127\3\2\2\2\u0127\u0129\3\2\2\2")
        buf.write("\u0128\u0126\3\2\2\2\u0129\u012c\7=\2\2\u012a\u012b\7")
        buf.write("&\2\2\u012b\u012d\5H%\2\u012c\u012a\3\2\2\2\u012c\u012d")
        buf.write("\3\2\2\2\u012d\u0158\3\2\2\2\u012e\u012f\7\66\2\2\u012f")
        buf.write("\u0130\7<\2\2\u0130\u0131\7<\2\2\u0131\u0136\7\60\2\2")
        buf.write("\u0132\u0133\7/\2\2\u0133\u0135\7\60\2\2\u0134\u0132\3")
        buf.write("\2\2\2\u0135\u0138\3\2\2\2\u0136\u0134\3\2\2\2\u0136\u0137")
        buf.write("\3\2\2\2\u0137\u0139\3\2\2\2\u0138\u0136\3\2\2\2\u0139")
        buf.write("\u013a\7=\2\2\u013a\u0158\7=\2\2\u013b\u013c\7\66\2\2")
        buf.write("\u013c\u013d\7&\2\2\u013d\u0158\58\35\2\u013e\u013f\5")
        buf.write("8\35\2\u013f\u0140\7&\2\2\u0140\u0141\58\35\2\u0141\u0158")
        buf.write("\3\2\2\2\u0142\u0143\58\35\2\u0143\u0144\7/\2\2\u0144")
        buf.write("\u0145\58\35\2\u0145\u0158\3\2\2\2\u0146\u0147\58\35\2")
        buf.write("\u0147\u0148\7:\2\2\u0148\u0149\58\35\2\u0149\u014a\7")
        buf.write(";\2\2\u014a\u0158\3\2\2\2\u014b\u014c\58\35\2\u014c\u014d")
        buf.write("\7<\2\2\u014d\u014e\58\35\2\u014e\u014f\7=\2\2\u014f\u0158")
        buf.write("\3\2\2\2\u0150\u0151\58\35\2\u0151\u0152\5\64\33\2\u0152")
        buf.write("\u0153\58\35\2\u0153\u0158\3\2\2\2\u0154\u0158\5D#\2\u0155")
        buf.write("\u0158\5F$\2\u0156\u0158\5T+\2\u0157\u011a\3\2\2\2\u0157")
        buf.write("\u011c\3\2\2\2\u0157\u012e\3\2\2\2\u0157\u013b\3\2\2\2")
        buf.write("\u0157\u013e\3\2\2\2\u0157\u0142\3\2\2\2\u0157\u0146\3")
        buf.write("\2\2\2\u0157\u014b\3\2\2\2\u0157\u0150\3\2\2\2\u0157\u0154")
        buf.write("\3\2\2\2\u0157\u0155\3\2\2\2\u0157\u0156\3\2\2\2\u0158")
        buf.write(";\3\2\2\2\u0159\u015a\7\67\2\2\u015a\u015b\7<\2\2\u015b")
        buf.write("\u015c\7\61\2\2\u015c\u015d\7=\2\2\u015d=\3\2\2\2\u015e")
        buf.write("\u0160\7<\2\2\u015f\u0161\5@!\2\u0160\u015f\3\2\2\2\u0160")
        buf.write("\u0161\3\2\2\2\u0161\u0162\3\2\2\2\u0162\u0163\7=\2\2")
        buf.write("\u0163?\3\2\2\2\u0164\u0169\5B\"\2\u0165\u0166\7/\2\2")
        buf.write("\u0166\u0168\5B\"\2\u0167\u0165\3\2\2\2\u0168\u016b\3")
        buf.write("\2\2\2\u0169\u0167\3\2\2\2\u0169\u016a\3\2\2\2\u016aA")
        buf.write("\3\2\2\2\u016b\u0169\3\2\2\2\u016c\u016d\t\5\2\2\u016d")
        buf.write("C\3\2\2\2\u016e\u016f\7:\2\2\u016f\u0170\58\35\2\u0170")
        buf.write("\u0171\7;\2\2\u0171E\3\2\2\2\u0172\u0173\7<\2\2\u0173")
        buf.write("\u0174\58\35\2\u0174\u0175\7=\2\2\u0175G\3\2\2\2\u0176")
        buf.write("\u0177\7\67\2\2\u0177\u0179\7&\2\2\u0178\u0176\3\2\2\2")
        buf.write("\u0178\u0179\3\2\2\2\u0179\u017a\3\2\2\2\u017a\u017b\7")
        buf.write("\67\2\2\u017b\u017c\7:\2\2\u017c\u017d\5L\'\2\u017d\u017e")
        buf.write("\7;\2\2\u017eI\3\2\2\2\u017f\u0180\5R*\2\u0180\u0181\7")
        buf.write(":\2\2\u0181\u0182\58\35\2\u0182\u0183\7;\2\2\u0183K\3")
        buf.write("\2\2\2\u0184\u0189\58\35\2\u0185\u0186\7/\2\2\u0186\u0188")
        buf.write("\58\35\2\u0187\u0185\3\2\2\2\u0188\u018b\3\2\2\2\u0189")
        buf.write("\u0187\3\2\2\2\u0189\u018a\3\2\2\2\u018a\u018d\3\2\2\2")
        buf.write("\u018b\u0189\3\2\2\2\u018c\u0184\3\2\2\2\u018d\u0190\3")
        buf.write("\2\2\2\u018e\u018c\3\2\2\2\u018e\u018f\3\2\2\2\u018fM")
        buf.write("\3\2\2\2\u0190\u018e\3\2\2\2\u0191\u0193\7\66\2\2\u0192")
        buf.write("\u0194\58\35\2\u0193\u0192\3\2\2\2\u0194\u0195\3\2\2\2")
        buf.write("\u0195\u0193\3\2\2\2\u0195\u0196\3\2\2\2\u0196O\3\2\2")
        buf.write("\2\u0197\u0199\7\'\2\2\u0198\u019a\58\35\2\u0199\u0198")
        buf.write("\3\2\2\2\u0199\u019a\3\2\2\2\u019a\u019d\3\2\2\2\u019b")
        buf.write("\u019c\7(\2\2\u019c\u019e\58\35\2\u019d\u019b\3\2\2\2")
        buf.write("\u019d\u019e\3\2\2\2\u019eQ\3\2\2\2\u019f\u01a0\t\6\2")
        buf.write("\2\u01a0S\3\2\2\2\u01a1\u01a2\7\67\2\2\u01a2\u01a3\7&")
        buf.write("\2\2\u01a3\u01a4\7\67\2\2\u01a4U\3\2\2\2\"XZakq\u0083")
        buf.write("\u0090\u009b\u00a1\u00ae\u00b4\u00c1\u00ce\u00d7\u00db")
        buf.write("\u00e2\u00ec\u00f5\u010f\u0117\u0126\u012c\u0136\u0157")
        buf.write("\u0160\u0169\u0178\u0189\u018e\u0195\u0199\u019d")
        return buf.getvalue()


class Python3d3Parser ( Parser ):

    grammarFileName = "Python3d3.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "':'", "'break'", "'continue'", "'return'", 
                     "'raise'", "'if'", "'elif'", "'else'", "'while'", "'for'", 
                     "'in'", "'try:'", "'range'", "'print'", "'and'", "'or'", 
                     "'not'", "'<'", "'>'", "'=='", "'>='", "'<='", "'!='", 
                     "'+'", "'-'", "'*'", "'/'", "'%'", "'**'", "'&'", "'|'", 
                     "'~'", "'^'", "'<<'", "'>>'", "'.'", "'except'", "'as'", 
                     "'int'", "'str'", "'list'", "'float'", "'bool'", "'None'", 
                     "','", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'('", "')'", "'['", "']'", 
                     "'{'", "'}'", "'='" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "SEP", "STRING", "NUMBER", "FLOAT", "BOOL", 
                      "INTEGER", "NEWLINE", "GRZLYNAME", "NAME", "STRING_LITERAL", 
                      "DECIMAL_INTEGER", "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACK", 
                      "CLOSE_BRACK", "OPEN_BRACE", "CLOSE_BRACE", "ASSIGN_EQUAL", 
                      "SKIP_", "UNKNOWN_CHAR", "INDENT", "DEDENT" ]

    RULE_file_input = 0
    RULE_stmt = 1
    RULE_simple_stmt = 2
    RULE_small_stmt = 3
    RULE_assignment_stmt = 4
    RULE_initialization = 5
    RULE_declaration = 6
    RULE_nontype_initialization = 7
    RULE_lst_assignment = 8
    RULE_flow_stmt = 9
    RULE_break_stmt = 10
    RULE_continue_stmt = 11
    RULE_return_stmt = 12
    RULE_raise_stmt = 13
    RULE_compound_stmt = 14
    RULE_if_stmt = 15
    RULE_while_stmt = 16
    RULE_for_stmt = 17
    RULE_exception_stmt = 18
    RULE_suite = 19
    RULE_rang = 20
    RULE_ob_test = 21
    RULE_test = 22
    RULE_print_stmt = 23
    RULE_log_op = 24
    RULE_comp_op = 25
    RULE_calc_op = 26
    RULE_expr = 27
    RULE_grzly_expr = 28
    RULE_list_dec = 29
    RULE_list_expr = 30
    RULE_elems = 31
    RULE_elem = 32
    RULE_parenthesis_expr = 33
    RULE_brackets_expr = 34
    RULE_func_call = 35
    RULE_typecast = 36
    RULE_params = 37
    RULE_grzly_stmt = 38
    RULE_except_stmt = 39
    RULE_typ = 40
    RULE_db_reference = 41

    ruleNames =  [ "file_input", "stmt", "simple_stmt", "small_stmt", "assignment_stmt", 
                   "initialization", "declaration", "nontype_initialization", 
                   "lst_assignment", "flow_stmt", "break_stmt", "continue_stmt", 
                   "return_stmt", "raise_stmt", "compound_stmt", "if_stmt", 
                   "while_stmt", "for_stmt", "exception_stmt", "suite", 
                   "rang", "ob_test", "test", "print_stmt", "log_op", "comp_op", 
                   "calc_op", "expr", "grzly_expr", "list_dec", "list_expr", 
                   "elems", "elem", "parenthesis_expr", "brackets_expr", 
                   "func_call", "typecast", "params", "grzly_stmt", "except_stmt", 
                   "typ", "db_reference" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    T__37=38
    T__38=39
    T__39=40
    T__40=41
    T__41=42
    T__42=43
    T__43=44
    SEP=45
    STRING=46
    NUMBER=47
    FLOAT=48
    BOOL=49
    INTEGER=50
    NEWLINE=51
    GRZLYNAME=52
    NAME=53
    STRING_LITERAL=54
    DECIMAL_INTEGER=55
    OPEN_PAREN=56
    CLOSE_PAREN=57
    OPEN_BRACK=58
    CLOSE_BRACK=59
    OPEN_BRACE=60
    CLOSE_BRACE=61
    ASSIGN_EQUAL=62
    SKIP_=63
    UNKNOWN_CHAR=64
    INDENT=65
    DEDENT=66

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class File_inputContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(Python3d3Parser.EOF, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.NEWLINE)
            else:
                return self.getToken(Python3d3Parser.NEWLINE, i)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.StmtContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.StmtContext,i)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_file_input

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFile_input" ):
                listener.enterFile_input(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFile_input" ):
                listener.exitFile_input(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFile_input" ):
                return visitor.visitFile_input(self)
            else:
                return visitor.visitChildren(self)




    def file_input(self):

        localctx = Python3d3Parser.File_inputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_file_input)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__1) | (1 << Python3d3Parser.T__2) | (1 << Python3d3Parser.T__3) | (1 << Python3d3Parser.T__4) | (1 << Python3d3Parser.T__5) | (1 << Python3d3Parser.T__8) | (1 << Python3d3Parser.T__9) | (1 << Python3d3Parser.T__11) | (1 << Python3d3Parser.T__13) | (1 << Python3d3Parser.NEWLINE) | (1 << Python3d3Parser.GRZLYNAME) | (1 << Python3d3Parser.NAME))) != 0):
                self.state = 86
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [Python3d3Parser.NEWLINE]:
                    self.state = 84
                    self.match(Python3d3Parser.NEWLINE)
                    pass
                elif token in [Python3d3Parser.T__1, Python3d3Parser.T__2, Python3d3Parser.T__3, Python3d3Parser.T__4, Python3d3Parser.T__5, Python3d3Parser.T__8, Python3d3Parser.T__9, Python3d3Parser.T__11, Python3d3Parser.T__13, Python3d3Parser.GRZLYNAME, Python3d3Parser.NAME]:
                    self.state = 85
                    self.stmt()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 90
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 91
            self.match(Python3d3Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Simple_stmtContext,0)


        def compound_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Compound_stmtContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmt" ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmt" ):
                listener.exitStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = Python3d3Parser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stmt)
        try:
            self.state = 95
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [Python3d3Parser.T__1, Python3d3Parser.T__2, Python3d3Parser.T__3, Python3d3Parser.T__4, Python3d3Parser.T__13, Python3d3Parser.GRZLYNAME, Python3d3Parser.NAME]:
                self.enterOuterAlt(localctx, 1)
                self.state = 93
                self.simple_stmt()
                pass
            elif token in [Python3d3Parser.T__5, Python3d3Parser.T__8, Python3d3Parser.T__9, Python3d3Parser.T__11]:
                self.enterOuterAlt(localctx, 2)
                self.state = 94
                self.compound_stmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Simple_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def small_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Small_stmtContext,0)


        def NEWLINE(self):
            return self.getToken(Python3d3Parser.NEWLINE, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_simple_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimple_stmt" ):
                listener.enterSimple_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimple_stmt" ):
                listener.exitSimple_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimple_stmt" ):
                return visitor.visitSimple_stmt(self)
            else:
                return visitor.visitChildren(self)




    def simple_stmt(self):

        localctx = Python3d3Parser.Simple_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_simple_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            self.small_stmt()
            self.state = 98
            self.match(Python3d3Parser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Small_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Assignment_stmtContext,0)


        def flow_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Flow_stmtContext,0)


        def print_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Print_stmtContext,0)


        def func_call(self):
            return self.getTypedRuleContext(Python3d3Parser.Func_callContext,0)


        def grzly_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Grzly_stmtContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_small_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSmall_stmt" ):
                listener.enterSmall_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSmall_stmt" ):
                listener.exitSmall_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSmall_stmt" ):
                return visitor.visitSmall_stmt(self)
            else:
                return visitor.visitChildren(self)




    def small_stmt(self):

        localctx = Python3d3Parser.Small_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_small_stmt)
        try:
            self.state = 105
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 100
                self.assignment_stmt()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 101
                self.flow_stmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 102
                self.print_stmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 103
                self.func_call()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 104
                self.grzly_stmt()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Assignment_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def initialization(self):
            return self.getTypedRuleContext(Python3d3Parser.InitializationContext,0)


        def declaration(self):
            return self.getTypedRuleContext(Python3d3Parser.DeclarationContext,0)


        def nontype_initialization(self):
            return self.getTypedRuleContext(Python3d3Parser.Nontype_initializationContext,0)


        def lst_assignment(self):
            return self.getTypedRuleContext(Python3d3Parser.Lst_assignmentContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_assignment_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment_stmt" ):
                listener.enterAssignment_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment_stmt" ):
                listener.exitAssignment_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment_stmt" ):
                return visitor.visitAssignment_stmt(self)
            else:
                return visitor.visitChildren(self)




    def assignment_stmt(self):

        localctx = Python3d3Parser.Assignment_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_assignment_stmt)
        try:
            self.state = 111
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 107
                self.initialization()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 108
                self.declaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 109
                self.nontype_initialization()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 110
                self.lst_assignment()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InitializationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(Python3d3Parser.NAME, 0)

        def typ(self):
            return self.getTypedRuleContext(Python3d3Parser.TypContext,0)


        def ASSIGN_EQUAL(self):
            return self.getToken(Python3d3Parser.ASSIGN_EQUAL, 0)

        def expr(self):
            return self.getTypedRuleContext(Python3d3Parser.ExprContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_initialization

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInitialization" ):
                listener.enterInitialization(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInitialization" ):
                listener.exitInitialization(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInitialization" ):
                return visitor.visitInitialization(self)
            else:
                return visitor.visitChildren(self)




    def initialization(self):

        localctx = Python3d3Parser.InitializationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_initialization)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.match(Python3d3Parser.NAME)
            self.state = 114
            self.match(Python3d3Parser.T__0)
            self.state = 115
            self.typ()
            self.state = 116
            self.match(Python3d3Parser.ASSIGN_EQUAL)
            self.state = 117
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(Python3d3Parser.NAME, 0)

        def typ(self):
            return self.getTypedRuleContext(Python3d3Parser.TypContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaration" ):
                return visitor.visitDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def declaration(self):

        localctx = Python3d3Parser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self.match(Python3d3Parser.NAME)
            self.state = 120
            self.match(Python3d3Parser.T__0)
            self.state = 121
            self.typ()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Nontype_initializationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GRZLYNAME(self):
            return self.getToken(Python3d3Parser.GRZLYNAME, 0)

        def ASSIGN_EQUAL(self):
            return self.getToken(Python3d3Parser.ASSIGN_EQUAL, 0)

        def grzly_expr(self):
            return self.getTypedRuleContext(Python3d3Parser.Grzly_exprContext,0)


        def NAME(self):
            return self.getToken(Python3d3Parser.NAME, 0)

        def expr(self):
            return self.getTypedRuleContext(Python3d3Parser.ExprContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_nontype_initialization

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNontype_initialization" ):
                listener.enterNontype_initialization(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNontype_initialization" ):
                listener.exitNontype_initialization(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNontype_initialization" ):
                return visitor.visitNontype_initialization(self)
            else:
                return visitor.visitChildren(self)




    def nontype_initialization(self):

        localctx = Python3d3Parser.Nontype_initializationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_nontype_initialization)
        try:
            self.state = 129
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [Python3d3Parser.GRZLYNAME]:
                self.enterOuterAlt(localctx, 1)
                self.state = 123
                self.match(Python3d3Parser.GRZLYNAME)
                self.state = 124
                self.match(Python3d3Parser.ASSIGN_EQUAL)
                self.state = 125
                self.grzly_expr()
                pass
            elif token in [Python3d3Parser.NAME]:
                self.enterOuterAlt(localctx, 2)
                self.state = 126
                self.match(Python3d3Parser.NAME)
                self.state = 127
                self.match(Python3d3Parser.ASSIGN_EQUAL)
                self.state = 128
                self.expr(0)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Lst_assignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(Python3d3Parser.NAME, 0)

        def OPEN_BRACK(self):
            return self.getToken(Python3d3Parser.OPEN_BRACK, 0)

        def NUMBER(self):
            return self.getToken(Python3d3Parser.NUMBER, 0)

        def CLOSE_BRACK(self):
            return self.getToken(Python3d3Parser.CLOSE_BRACK, 0)

        def ASSIGN_EQUAL(self):
            return self.getToken(Python3d3Parser.ASSIGN_EQUAL, 0)

        def expr(self):
            return self.getTypedRuleContext(Python3d3Parser.ExprContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_lst_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLst_assignment" ):
                listener.enterLst_assignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLst_assignment" ):
                listener.exitLst_assignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLst_assignment" ):
                return visitor.visitLst_assignment(self)
            else:
                return visitor.visitChildren(self)




    def lst_assignment(self):

        localctx = Python3d3Parser.Lst_assignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_lst_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.match(Python3d3Parser.NAME)
            self.state = 132
            self.match(Python3d3Parser.OPEN_BRACK)
            self.state = 133
            self.match(Python3d3Parser.NUMBER)
            self.state = 134
            self.match(Python3d3Parser.CLOSE_BRACK)
            self.state = 135
            self.match(Python3d3Parser.ASSIGN_EQUAL)
            self.state = 136
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Flow_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def break_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Break_stmtContext,0)


        def continue_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Continue_stmtContext,0)


        def return_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Return_stmtContext,0)


        def raise_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Raise_stmtContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_flow_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFlow_stmt" ):
                listener.enterFlow_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFlow_stmt" ):
                listener.exitFlow_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFlow_stmt" ):
                return visitor.visitFlow_stmt(self)
            else:
                return visitor.visitChildren(self)




    def flow_stmt(self):

        localctx = Python3d3Parser.Flow_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_flow_stmt)
        try:
            self.state = 142
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [Python3d3Parser.T__1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 138
                self.break_stmt()
                pass
            elif token in [Python3d3Parser.T__2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 139
                self.continue_stmt()
                pass
            elif token in [Python3d3Parser.T__3]:
                self.enterOuterAlt(localctx, 3)
                self.state = 140
                self.return_stmt()
                pass
            elif token in [Python3d3Parser.T__4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 141
                self.raise_stmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Break_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return Python3d3Parser.RULE_break_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreak_stmt" ):
                listener.enterBreak_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreak_stmt" ):
                listener.exitBreak_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreak_stmt" ):
                return visitor.visitBreak_stmt(self)
            else:
                return visitor.visitChildren(self)




    def break_stmt(self):

        localctx = Python3d3Parser.Break_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_break_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 144
            self.match(Python3d3Parser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Continue_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return Python3d3Parser.RULE_continue_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinue_stmt" ):
                listener.enterContinue_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinue_stmt" ):
                listener.exitContinue_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinue_stmt" ):
                return visitor.visitContinue_stmt(self)
            else:
                return visitor.visitChildren(self)




    def continue_stmt(self):

        localctx = Python3d3Parser.Continue_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_continue_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 146
            self.match(Python3d3Parser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Return_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(Python3d3Parser.ExprContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_return_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturn_stmt" ):
                listener.enterReturn_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturn_stmt" ):
                listener.exitReturn_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturn_stmt" ):
                return visitor.visitReturn_stmt(self)
            else:
                return visitor.visitChildren(self)




    def return_stmt(self):

        localctx = Python3d3Parser.Return_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_return_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            self.match(Python3d3Parser.T__3)
            self.state = 149
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Raise_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(Python3d3Parser.NAME, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_raise_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRaise_stmt" ):
                listener.enterRaise_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRaise_stmt" ):
                listener.exitRaise_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRaise_stmt" ):
                return visitor.visitRaise_stmt(self)
            else:
                return visitor.visitChildren(self)




    def raise_stmt(self):

        localctx = Python3d3Parser.Raise_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_raise_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self.match(Python3d3Parser.T__4)
            self.state = 153
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Python3d3Parser.NAME:
                self.state = 152
                self.match(Python3d3Parser.NAME)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Compound_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def if_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.If_stmtContext,0)


        def while_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.While_stmtContext,0)


        def for_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.For_stmtContext,0)


        def exception_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Exception_stmtContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_compound_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompound_stmt" ):
                listener.enterCompound_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompound_stmt" ):
                listener.exitCompound_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompound_stmt" ):
                return visitor.visitCompound_stmt(self)
            else:
                return visitor.visitChildren(self)




    def compound_stmt(self):

        localctx = Python3d3Parser.Compound_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_compound_stmt)
        try:
            self.state = 159
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [Python3d3Parser.T__5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 155
                self.if_stmt()
                pass
            elif token in [Python3d3Parser.T__8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 156
                self.while_stmt()
                pass
            elif token in [Python3d3Parser.T__9]:
                self.enterOuterAlt(localctx, 3)
                self.state = 157
                self.for_stmt()
                pass
            elif token in [Python3d3Parser.T__11]:
                self.enterOuterAlt(localctx, 4)
                self.state = 158
                self.exception_stmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class If_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ob_test(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.Ob_testContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.Ob_testContext,i)


        def suite(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.SuiteContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.SuiteContext,i)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_if_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIf_stmt" ):
                listener.enterIf_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIf_stmt" ):
                listener.exitIf_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIf_stmt" ):
                return visitor.visitIf_stmt(self)
            else:
                return visitor.visitChildren(self)




    def if_stmt(self):

        localctx = Python3d3Parser.If_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_if_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self.match(Python3d3Parser.T__5)
            self.state = 162
            self.ob_test()
            self.state = 163
            self.match(Python3d3Parser.T__0)
            self.state = 164
            self.suite()
            self.state = 172
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==Python3d3Parser.T__6:
                self.state = 165
                self.match(Python3d3Parser.T__6)
                self.state = 166
                self.ob_test()
                self.state = 167
                self.match(Python3d3Parser.T__0)
                self.state = 168
                self.suite()
                self.state = 174
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 178
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Python3d3Parser.T__7:
                self.state = 175
                self.match(Python3d3Parser.T__7)
                self.state = 176
                self.match(Python3d3Parser.T__0)
                self.state = 177
                self.suite()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class While_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ob_test(self):
            return self.getTypedRuleContext(Python3d3Parser.Ob_testContext,0)


        def suite(self):
            return self.getTypedRuleContext(Python3d3Parser.SuiteContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_while_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhile_stmt" ):
                listener.enterWhile_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhile_stmt" ):
                listener.exitWhile_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhile_stmt" ):
                return visitor.visitWhile_stmt(self)
            else:
                return visitor.visitChildren(self)




    def while_stmt(self):

        localctx = Python3d3Parser.While_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_while_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 180
            self.match(Python3d3Parser.T__8)
            self.state = 181
            self.ob_test()
            self.state = 182
            self.match(Python3d3Parser.T__0)
            self.state = 183
            self.suite()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class For_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(Python3d3Parser.NAME, 0)

        def suite(self):
            return self.getTypedRuleContext(Python3d3Parser.SuiteContext,0)


        def expr(self):
            return self.getTypedRuleContext(Python3d3Parser.ExprContext,0)


        def rang(self):
            return self.getTypedRuleContext(Python3d3Parser.RangContext,0)


        def GRZLYNAME(self):
            return self.getToken(Python3d3Parser.GRZLYNAME, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_for_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFor_stmt" ):
                listener.enterFor_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFor_stmt" ):
                listener.exitFor_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFor_stmt" ):
                return visitor.visitFor_stmt(self)
            else:
                return visitor.visitChildren(self)




    def for_stmt(self):

        localctx = Python3d3Parser.For_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_for_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self.match(Python3d3Parser.T__9)
            self.state = 186
            self.match(Python3d3Parser.NAME)
            self.state = 187
            self.match(Python3d3Parser.T__10)
            self.state = 191
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [Python3d3Parser.T__38, Python3d3Parser.T__39, Python3d3Parser.T__40, Python3d3Parser.T__41, Python3d3Parser.T__42, Python3d3Parser.T__43, Python3d3Parser.STRING, Python3d3Parser.NUMBER, Python3d3Parser.FLOAT, Python3d3Parser.BOOL, Python3d3Parser.NAME, Python3d3Parser.OPEN_PAREN, Python3d3Parser.OPEN_BRACK]:
                self.state = 188
                self.expr(0)
                pass
            elif token in [Python3d3Parser.T__12]:
                self.state = 189
                self.rang()
                pass
            elif token in [Python3d3Parser.GRZLYNAME]:
                self.state = 190
                self.match(Python3d3Parser.GRZLYNAME)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 193
            self.match(Python3d3Parser.T__0)
            self.state = 194
            self.suite()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Exception_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def suite(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.SuiteContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.SuiteContext,i)


        def except_stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.Except_stmtContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.Except_stmtContext,i)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_exception_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterException_stmt" ):
                listener.enterException_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitException_stmt" ):
                listener.exitException_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitException_stmt" ):
                return visitor.visitException_stmt(self)
            else:
                return visitor.visitChildren(self)




    def exception_stmt(self):

        localctx = Python3d3Parser.Exception_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_exception_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            self.match(Python3d3Parser.T__11)
            self.state = 197
            self.suite()
            self.state = 204
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==Python3d3Parser.T__36:
                self.state = 198
                self.except_stmt()
                self.state = 199
                self.match(Python3d3Parser.T__0)
                self.state = 200
                self.suite()
                self.state = 206
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SuiteContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_stmt(self):
            return self.getTypedRuleContext(Python3d3Parser.Simple_stmtContext,0)


        def NEWLINE(self):
            return self.getToken(Python3d3Parser.NEWLINE, 0)

        def INDENT(self):
            return self.getToken(Python3d3Parser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(Python3d3Parser.DEDENT, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.StmtContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.StmtContext,i)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_suite

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSuite" ):
                listener.enterSuite(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSuite" ):
                listener.exitSuite(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSuite" ):
                return visitor.visitSuite(self)
            else:
                return visitor.visitChildren(self)




    def suite(self):

        localctx = Python3d3Parser.SuiteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_suite)
        self._la = 0 # Token type
        try:
            self.state = 217
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [Python3d3Parser.T__1, Python3d3Parser.T__2, Python3d3Parser.T__3, Python3d3Parser.T__4, Python3d3Parser.T__13, Python3d3Parser.GRZLYNAME, Python3d3Parser.NAME]:
                self.enterOuterAlt(localctx, 1)
                self.state = 207
                self.simple_stmt()
                pass
            elif token in [Python3d3Parser.NEWLINE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 208
                self.match(Python3d3Parser.NEWLINE)
                self.state = 209
                self.match(Python3d3Parser.INDENT)
                self.state = 211 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 210
                    self.stmt()
                    self.state = 213 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__1) | (1 << Python3d3Parser.T__2) | (1 << Python3d3Parser.T__3) | (1 << Python3d3Parser.T__4) | (1 << Python3d3Parser.T__5) | (1 << Python3d3Parser.T__8) | (1 << Python3d3Parser.T__9) | (1 << Python3d3Parser.T__11) | (1 << Python3d3Parser.T__13) | (1 << Python3d3Parser.GRZLYNAME) | (1 << Python3d3Parser.NAME))) != 0)):
                        break

                self.state = 215
                self.match(Python3d3Parser.DEDENT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RangContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(Python3d3Parser.OPEN_PAREN, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.ExprContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.ExprContext,i)


        def CLOSE_PAREN(self):
            return self.getToken(Python3d3Parser.CLOSE_PAREN, 0)

        def SEP(self):
            return self.getToken(Python3d3Parser.SEP, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_rang

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRang" ):
                listener.enterRang(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRang" ):
                listener.exitRang(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRang" ):
                return visitor.visitRang(self)
            else:
                return visitor.visitChildren(self)




    def rang(self):

        localctx = Python3d3Parser.RangContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_rang)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 219
            self.match(Python3d3Parser.T__12)
            self.state = 220
            self.match(Python3d3Parser.OPEN_PAREN)
            self.state = 221
            self.expr(0)
            self.state = 224
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Python3d3Parser.SEP:
                self.state = 222
                self.match(Python3d3Parser.SEP)
                self.state = 223
                self.expr(0)


            self.state = 226
            self.match(Python3d3Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Ob_testContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def test(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.TestContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.TestContext,i)


        def log_op(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.Log_opContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.Log_opContext,i)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_ob_test

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOb_test" ):
                listener.enterOb_test(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOb_test" ):
                listener.exitOb_test(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOb_test" ):
                return visitor.visitOb_test(self)
            else:
                return visitor.visitChildren(self)




    def ob_test(self):

        localctx = Python3d3Parser.Ob_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_ob_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 228
            self.test()
            self.state = 234
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__14) | (1 << Python3d3Parser.T__15) | (1 << Python3d3Parser.T__16))) != 0):
                self.state = 229
                self.log_op()
                self.state = 230
                self.test()
                self.state = 236
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.ExprContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.ExprContext,i)


        def comp_op(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.Comp_opContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.Comp_opContext,i)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_test

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTest" ):
                listener.enterTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTest" ):
                listener.exitTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTest" ):
                return visitor.visitTest(self)
            else:
                return visitor.visitChildren(self)




    def test(self):

        localctx = Python3d3Parser.TestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 237
            self.expr(0)
            self.state = 243
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__17) | (1 << Python3d3Parser.T__18) | (1 << Python3d3Parser.T__19) | (1 << Python3d3Parser.T__20) | (1 << Python3d3Parser.T__21) | (1 << Python3d3Parser.T__22))) != 0):
                self.state = 238
                self.comp_op()
                self.state = 239
                self.expr(0)
                self.state = 245
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Print_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(Python3d3Parser.OPEN_PAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(Python3d3Parser.ExprContext,0)


        def CLOSE_PAREN(self):
            return self.getToken(Python3d3Parser.CLOSE_PAREN, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_print_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrint_stmt" ):
                listener.enterPrint_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrint_stmt" ):
                listener.exitPrint_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrint_stmt" ):
                return visitor.visitPrint_stmt(self)
            else:
                return visitor.visitChildren(self)




    def print_stmt(self):

        localctx = Python3d3Parser.Print_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_print_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 246
            self.match(Python3d3Parser.T__13)
            self.state = 247
            self.match(Python3d3Parser.OPEN_PAREN)
            self.state = 248
            self.expr(0)
            self.state = 249
            self.match(Python3d3Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Log_opContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return Python3d3Parser.RULE_log_op

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLog_op" ):
                listener.enterLog_op(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLog_op" ):
                listener.exitLog_op(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLog_op" ):
                return visitor.visitLog_op(self)
            else:
                return visitor.visitChildren(self)




    def log_op(self):

        localctx = Python3d3Parser.Log_opContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_log_op)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 251
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__14) | (1 << Python3d3Parser.T__15) | (1 << Python3d3Parser.T__16))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Comp_opContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return Python3d3Parser.RULE_comp_op

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComp_op" ):
                listener.enterComp_op(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComp_op" ):
                listener.exitComp_op(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComp_op" ):
                return visitor.visitComp_op(self)
            else:
                return visitor.visitChildren(self)




    def comp_op(self):

        localctx = Python3d3Parser.Comp_opContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_comp_op)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 253
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__17) | (1 << Python3d3Parser.T__18) | (1 << Python3d3Parser.T__19) | (1 << Python3d3Parser.T__20) | (1 << Python3d3Parser.T__21) | (1 << Python3d3Parser.T__22))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Calc_opContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return Python3d3Parser.RULE_calc_op

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCalc_op" ):
                listener.enterCalc_op(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCalc_op" ):
                listener.exitCalc_op(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCalc_op" ):
                return visitor.visitCalc_op(self)
            else:
                return visitor.visitChildren(self)




    def calc_op(self):

        localctx = Python3d3Parser.Calc_opContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_calc_op)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 255
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__23) | (1 << Python3d3Parser.T__24) | (1 << Python3d3Parser.T__25) | (1 << Python3d3Parser.T__26) | (1 << Python3d3Parser.T__27) | (1 << Python3d3Parser.T__28) | (1 << Python3d3Parser.T__29) | (1 << Python3d3Parser.T__30) | (1 << Python3d3Parser.T__31) | (1 << Python3d3Parser.T__32) | (1 << Python3d3Parser.T__33) | (1 << Python3d3Parser.T__34))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(Python3d3Parser.NAME, 0)

        def STRING(self):
            return self.getToken(Python3d3Parser.STRING, 0)

        def FLOAT(self):
            return self.getToken(Python3d3Parser.FLOAT, 0)

        def NUMBER(self):
            return self.getToken(Python3d3Parser.NUMBER, 0)

        def BOOL(self):
            return self.getToken(Python3d3Parser.BOOL, 0)

        def list_expr(self):
            return self.getTypedRuleContext(Python3d3Parser.List_exprContext,0)


        def list_dec(self):
            return self.getTypedRuleContext(Python3d3Parser.List_decContext,0)


        def db_reference(self):
            return self.getTypedRuleContext(Python3d3Parser.Db_referenceContext,0)


        def typecast(self):
            return self.getTypedRuleContext(Python3d3Parser.TypecastContext,0)


        def parenthesis_expr(self):
            return self.getTypedRuleContext(Python3d3Parser.Parenthesis_exprContext,0)


        def func_call(self):
            return self.getTypedRuleContext(Python3d3Parser.Func_callContext,0)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.ExprContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.ExprContext,i)


        def calc_op(self):
            return self.getTypedRuleContext(Python3d3Parser.Calc_opContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = Python3d3Parser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 54
        self.enterRecursionRule(localctx, 54, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 269
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.state = 258
                self.match(Python3d3Parser.NAME)
                pass

            elif la_ == 2:
                self.state = 259
                self.match(Python3d3Parser.STRING)
                pass

            elif la_ == 3:
                self.state = 260
                self.match(Python3d3Parser.FLOAT)
                pass

            elif la_ == 4:
                self.state = 261
                self.match(Python3d3Parser.NUMBER)
                pass

            elif la_ == 5:
                self.state = 262
                self.match(Python3d3Parser.BOOL)
                pass

            elif la_ == 6:
                self.state = 263
                self.list_expr()
                pass

            elif la_ == 7:
                self.state = 264
                self.list_dec()
                pass

            elif la_ == 8:
                self.state = 265
                self.db_reference()
                pass

            elif la_ == 9:
                self.state = 266
                self.typecast()
                pass

            elif la_ == 10:
                self.state = 267
                self.parenthesis_expr()
                pass

            elif la_ == 11:
                self.state = 268
                self.func_call()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 277
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,19,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = Python3d3Parser.ExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                    self.state = 271
                    if not self.precpred(self._ctx, 12):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                    self.state = 272
                    self.calc_op()
                    self.state = 273
                    self.expr(13) 
                self.state = 279
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,19,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Grzly_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GRZLYNAME(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.GRZLYNAME)
            else:
                return self.getToken(Python3d3Parser.GRZLYNAME, i)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.ExprContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.ExprContext,i)


        def OPEN_BRACK(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.OPEN_BRACK)
            else:
                return self.getToken(Python3d3Parser.OPEN_BRACK, i)

        def CLOSE_BRACK(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.CLOSE_BRACK)
            else:
                return self.getToken(Python3d3Parser.CLOSE_BRACK, i)

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.NAME)
            else:
                return self.getToken(Python3d3Parser.NAME, i)

        def comp_op(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.Comp_opContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.Comp_opContext,i)


        def func_call(self):
            return self.getTypedRuleContext(Python3d3Parser.Func_callContext,0)


        def STRING(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.STRING)
            else:
                return self.getToken(Python3d3Parser.STRING, i)

        def SEP(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.SEP)
            else:
                return self.getToken(Python3d3Parser.SEP, i)

        def OPEN_PAREN(self):
            return self.getToken(Python3d3Parser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(Python3d3Parser.CLOSE_PAREN, 0)

        def parenthesis_expr(self):
            return self.getTypedRuleContext(Python3d3Parser.Parenthesis_exprContext,0)


        def brackets_expr(self):
            return self.getTypedRuleContext(Python3d3Parser.Brackets_exprContext,0)


        def db_reference(self):
            return self.getTypedRuleContext(Python3d3Parser.Db_referenceContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_grzly_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGrzly_expr" ):
                listener.enterGrzly_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGrzly_expr" ):
                listener.exitGrzly_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGrzly_expr" ):
                return visitor.visitGrzly_expr(self)
            else:
                return visitor.visitChildren(self)




    def grzly_expr(self):

        localctx = Python3d3Parser.Grzly_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_grzly_expr)
        self._la = 0 # Token type
        try:
            self.state = 341
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 280
                self.match(Python3d3Parser.GRZLYNAME)
                self.state = 281
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 282
                self.match(Python3d3Parser.GRZLYNAME)
                self.state = 283
                self.match(Python3d3Parser.OPEN_BRACK)
                self.state = 292
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==Python3d3Parser.GRZLYNAME:
                    self.state = 284
                    self.match(Python3d3Parser.GRZLYNAME)
                    self.state = 285
                    self.match(Python3d3Parser.T__35)
                    self.state = 286
                    self.match(Python3d3Parser.NAME)
                    self.state = 287
                    self.comp_op()
                    self.state = 288
                    self.expr(0)
                    self.state = 294
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 295
                self.match(Python3d3Parser.CLOSE_BRACK)
                self.state = 298
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==Python3d3Parser.T__35:
                    self.state = 296
                    self.match(Python3d3Parser.T__35)
                    self.state = 297
                    self.func_call()


                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 300
                self.match(Python3d3Parser.GRZLYNAME)
                self.state = 301
                self.match(Python3d3Parser.OPEN_BRACK)
                self.state = 302
                self.match(Python3d3Parser.OPEN_BRACK)
                self.state = 303
                self.match(Python3d3Parser.STRING)
                self.state = 308
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==Python3d3Parser.SEP:
                    self.state = 304
                    self.match(Python3d3Parser.SEP)
                    self.state = 305
                    self.match(Python3d3Parser.STRING)
                    self.state = 310
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 311
                self.match(Python3d3Parser.CLOSE_BRACK)
                self.state = 312
                self.match(Python3d3Parser.CLOSE_BRACK)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 313
                self.match(Python3d3Parser.GRZLYNAME)
                self.state = 314
                self.match(Python3d3Parser.T__35)
                self.state = 315
                self.expr(0)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 316
                self.expr(0)
                self.state = 317
                self.match(Python3d3Parser.T__35)
                self.state = 318
                self.expr(0)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 320
                self.expr(0)
                self.state = 321
                self.match(Python3d3Parser.SEP)
                self.state = 322
                self.expr(0)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 324
                self.expr(0)
                self.state = 325
                self.match(Python3d3Parser.OPEN_PAREN)
                self.state = 326
                self.expr(0)
                self.state = 327
                self.match(Python3d3Parser.CLOSE_PAREN)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 329
                self.expr(0)
                self.state = 330
                self.match(Python3d3Parser.OPEN_BRACK)
                self.state = 331
                self.expr(0)
                self.state = 332
                self.match(Python3d3Parser.CLOSE_BRACK)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 334
                self.expr(0)

                self.state = 335
                self.comp_op()
                self.state = 336
                self.expr(0)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 338
                self.parenthesis_expr()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 339
                self.brackets_expr()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 340
                self.db_reference()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class List_decContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(Python3d3Parser.NAME, 0)

        def OPEN_BRACK(self):
            return self.getToken(Python3d3Parser.OPEN_BRACK, 0)

        def NUMBER(self):
            return self.getToken(Python3d3Parser.NUMBER, 0)

        def CLOSE_BRACK(self):
            return self.getToken(Python3d3Parser.CLOSE_BRACK, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_list_dec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterList_dec" ):
                listener.enterList_dec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitList_dec" ):
                listener.exitList_dec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitList_dec" ):
                return visitor.visitList_dec(self)
            else:
                return visitor.visitChildren(self)




    def list_dec(self):

        localctx = Python3d3Parser.List_decContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_list_dec)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 343
            self.match(Python3d3Parser.NAME)
            self.state = 344
            self.match(Python3d3Parser.OPEN_BRACK)
            self.state = 345
            self.match(Python3d3Parser.NUMBER)
            self.state = 346
            self.match(Python3d3Parser.CLOSE_BRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class List_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPEN_BRACK(self):
            return self.getToken(Python3d3Parser.OPEN_BRACK, 0)

        def CLOSE_BRACK(self):
            return self.getToken(Python3d3Parser.CLOSE_BRACK, 0)

        def elems(self):
            return self.getTypedRuleContext(Python3d3Parser.ElemsContext,0)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_list_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterList_expr" ):
                listener.enterList_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitList_expr" ):
                listener.exitList_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitList_expr" ):
                return visitor.visitList_expr(self)
            else:
                return visitor.visitChildren(self)




    def list_expr(self):

        localctx = Python3d3Parser.List_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_list_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 348
            self.match(Python3d3Parser.OPEN_BRACK)
            self.state = 350
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.STRING) | (1 << Python3d3Parser.NUMBER) | (1 << Python3d3Parser.FLOAT) | (1 << Python3d3Parser.BOOL) | (1 << Python3d3Parser.NAME))) != 0):
                self.state = 349
                self.elems()


            self.state = 352
            self.match(Python3d3Parser.CLOSE_BRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElemsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def elem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.ElemContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.ElemContext,i)


        def SEP(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.SEP)
            else:
                return self.getToken(Python3d3Parser.SEP, i)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_elems

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElems" ):
                listener.enterElems(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElems" ):
                listener.exitElems(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElems" ):
                return visitor.visitElems(self)
            else:
                return visitor.visitChildren(self)




    def elems(self):

        localctx = Python3d3Parser.ElemsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_elems)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 354
            self.elem()
            self.state = 359
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==Python3d3Parser.SEP:
                self.state = 355
                self.match(Python3d3Parser.SEP)
                self.state = 356
                self.elem()
                self.state = 361
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(Python3d3Parser.STRING, 0)

        def NUMBER(self):
            return self.getToken(Python3d3Parser.NUMBER, 0)

        def FLOAT(self):
            return self.getToken(Python3d3Parser.FLOAT, 0)

        def BOOL(self):
            return self.getToken(Python3d3Parser.BOOL, 0)

        def NAME(self):
            return self.getToken(Python3d3Parser.NAME, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_elem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElem" ):
                listener.enterElem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElem" ):
                listener.exitElem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElem" ):
                return visitor.visitElem(self)
            else:
                return visitor.visitChildren(self)




    def elem(self):

        localctx = Python3d3Parser.ElemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_elem)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 362
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.STRING) | (1 << Python3d3Parser.NUMBER) | (1 << Python3d3Parser.FLOAT) | (1 << Python3d3Parser.BOOL) | (1 << Python3d3Parser.NAME))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parenthesis_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(Python3d3Parser.OPEN_PAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(Python3d3Parser.ExprContext,0)


        def CLOSE_PAREN(self):
            return self.getToken(Python3d3Parser.CLOSE_PAREN, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_parenthesis_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenthesis_expr" ):
                listener.enterParenthesis_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenthesis_expr" ):
                listener.exitParenthesis_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenthesis_expr" ):
                return visitor.visitParenthesis_expr(self)
            else:
                return visitor.visitChildren(self)




    def parenthesis_expr(self):

        localctx = Python3d3Parser.Parenthesis_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_parenthesis_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 364
            self.match(Python3d3Parser.OPEN_PAREN)
            self.state = 365
            self.expr(0)
            self.state = 366
            self.match(Python3d3Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Brackets_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPEN_BRACK(self):
            return self.getToken(Python3d3Parser.OPEN_BRACK, 0)

        def expr(self):
            return self.getTypedRuleContext(Python3d3Parser.ExprContext,0)


        def CLOSE_BRACK(self):
            return self.getToken(Python3d3Parser.CLOSE_BRACK, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_brackets_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBrackets_expr" ):
                listener.enterBrackets_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBrackets_expr" ):
                listener.exitBrackets_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBrackets_expr" ):
                return visitor.visitBrackets_expr(self)
            else:
                return visitor.visitChildren(self)




    def brackets_expr(self):

        localctx = Python3d3Parser.Brackets_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_brackets_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 368
            self.match(Python3d3Parser.OPEN_BRACK)
            self.state = 369
            self.expr(0)
            self.state = 370
            self.match(Python3d3Parser.CLOSE_BRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Func_callContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.NAME)
            else:
                return self.getToken(Python3d3Parser.NAME, i)

        def OPEN_PAREN(self):
            return self.getToken(Python3d3Parser.OPEN_PAREN, 0)

        def params(self):
            return self.getTypedRuleContext(Python3d3Parser.ParamsContext,0)


        def CLOSE_PAREN(self):
            return self.getToken(Python3d3Parser.CLOSE_PAREN, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_func_call

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunc_call" ):
                listener.enterFunc_call(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunc_call" ):
                listener.exitFunc_call(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunc_call" ):
                return visitor.visitFunc_call(self)
            else:
                return visitor.visitChildren(self)




    def func_call(self):

        localctx = Python3d3Parser.Func_callContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_func_call)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 374
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,26,self._ctx)
            if la_ == 1:
                self.state = 372
                self.match(Python3d3Parser.NAME)
                self.state = 373
                self.match(Python3d3Parser.T__35)


            self.state = 376
            self.match(Python3d3Parser.NAME)
            self.state = 377
            self.match(Python3d3Parser.OPEN_PAREN)
            self.state = 378
            self.params()
            self.state = 379
            self.match(Python3d3Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypecastContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typ(self):
            return self.getTypedRuleContext(Python3d3Parser.TypContext,0)


        def OPEN_PAREN(self):
            return self.getToken(Python3d3Parser.OPEN_PAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(Python3d3Parser.ExprContext,0)


        def CLOSE_PAREN(self):
            return self.getToken(Python3d3Parser.CLOSE_PAREN, 0)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_typecast

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypecast" ):
                listener.enterTypecast(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypecast" ):
                listener.exitTypecast(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypecast" ):
                return visitor.visitTypecast(self)
            else:
                return visitor.visitChildren(self)




    def typecast(self):

        localctx = Python3d3Parser.TypecastContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_typecast)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 381
            self.typ()
            self.state = 382
            self.match(Python3d3Parser.OPEN_PAREN)
            self.state = 383
            self.expr(0)
            self.state = 384
            self.match(Python3d3Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.ExprContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.ExprContext,i)


        def SEP(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.SEP)
            else:
                return self.getToken(Python3d3Parser.SEP, i)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_params

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParams" ):
                listener.enterParams(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParams" ):
                listener.exitParams(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParams" ):
                return visitor.visitParams(self)
            else:
                return visitor.visitChildren(self)




    def params(self):

        localctx = Python3d3Parser.ParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 396
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__38) | (1 << Python3d3Parser.T__39) | (1 << Python3d3Parser.T__40) | (1 << Python3d3Parser.T__41) | (1 << Python3d3Parser.T__42) | (1 << Python3d3Parser.T__43) | (1 << Python3d3Parser.STRING) | (1 << Python3d3Parser.NUMBER) | (1 << Python3d3Parser.FLOAT) | (1 << Python3d3Parser.BOOL) | (1 << Python3d3Parser.NAME) | (1 << Python3d3Parser.OPEN_PAREN) | (1 << Python3d3Parser.OPEN_BRACK))) != 0):
                self.state = 386
                self.expr(0)
                self.state = 391
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==Python3d3Parser.SEP:
                    self.state = 387
                    self.match(Python3d3Parser.SEP)
                    self.state = 388
                    self.expr(0)
                    self.state = 393
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 398
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Grzly_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GRZLYNAME(self):
            return self.getToken(Python3d3Parser.GRZLYNAME, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.ExprContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.ExprContext,i)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_grzly_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGrzly_stmt" ):
                listener.enterGrzly_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGrzly_stmt" ):
                listener.exitGrzly_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGrzly_stmt" ):
                return visitor.visitGrzly_stmt(self)
            else:
                return visitor.visitChildren(self)




    def grzly_stmt(self):

        localctx = Python3d3Parser.Grzly_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_grzly_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 399
            self.match(Python3d3Parser.GRZLYNAME)
            self.state = 401 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 400
                self.expr(0)
                self.state = 403 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__38) | (1 << Python3d3Parser.T__39) | (1 << Python3d3Parser.T__40) | (1 << Python3d3Parser.T__41) | (1 << Python3d3Parser.T__42) | (1 << Python3d3Parser.T__43) | (1 << Python3d3Parser.STRING) | (1 << Python3d3Parser.NUMBER) | (1 << Python3d3Parser.FLOAT) | (1 << Python3d3Parser.BOOL) | (1 << Python3d3Parser.NAME) | (1 << Python3d3Parser.OPEN_PAREN) | (1 << Python3d3Parser.OPEN_BRACK))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Except_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Python3d3Parser.ExprContext)
            else:
                return self.getTypedRuleContext(Python3d3Parser.ExprContext,i)


        def getRuleIndex(self):
            return Python3d3Parser.RULE_except_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExcept_stmt" ):
                listener.enterExcept_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExcept_stmt" ):
                listener.exitExcept_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExcept_stmt" ):
                return visitor.visitExcept_stmt(self)
            else:
                return visitor.visitChildren(self)




    def except_stmt(self):

        localctx = Python3d3Parser.Except_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_except_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 405
            self.match(Python3d3Parser.T__36)
            self.state = 407
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__38) | (1 << Python3d3Parser.T__39) | (1 << Python3d3Parser.T__40) | (1 << Python3d3Parser.T__41) | (1 << Python3d3Parser.T__42) | (1 << Python3d3Parser.T__43) | (1 << Python3d3Parser.STRING) | (1 << Python3d3Parser.NUMBER) | (1 << Python3d3Parser.FLOAT) | (1 << Python3d3Parser.BOOL) | (1 << Python3d3Parser.NAME) | (1 << Python3d3Parser.OPEN_PAREN) | (1 << Python3d3Parser.OPEN_BRACK))) != 0):
                self.state = 406
                self.expr(0)


            self.state = 411
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Python3d3Parser.T__37:
                self.state = 409
                self.match(Python3d3Parser.T__37)
                self.state = 410
                self.expr(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return Python3d3Parser.RULE_typ

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTyp" ):
                listener.enterTyp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTyp" ):
                listener.exitTyp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTyp" ):
                return visitor.visitTyp(self)
            else:
                return visitor.visitChildren(self)




    def typ(self):

        localctx = Python3d3Parser.TypContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_typ)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 413
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Python3d3Parser.T__38) | (1 << Python3d3Parser.T__39) | (1 << Python3d3Parser.T__40) | (1 << Python3d3Parser.T__41) | (1 << Python3d3Parser.T__42) | (1 << Python3d3Parser.T__43))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Db_referenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(Python3d3Parser.NAME)
            else:
                return self.getToken(Python3d3Parser.NAME, i)

        def getRuleIndex(self):
            return Python3d3Parser.RULE_db_reference

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDb_reference" ):
                listener.enterDb_reference(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDb_reference" ):
                listener.exitDb_reference(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDb_reference" ):
                return visitor.visitDb_reference(self)
            else:
                return visitor.visitChildren(self)




    def db_reference(self):

        localctx = Python3d3Parser.Db_referenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_db_reference)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 415
            self.match(Python3d3Parser.NAME)
            self.state = 416
            self.match(Python3d3Parser.T__35)
            self.state = 417
            self.match(Python3d3Parser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[27] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 12)
         




