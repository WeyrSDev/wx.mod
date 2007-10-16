# MaxFacer.py - regenerate the Scintilla.h and SciLexer.h files from the Scintilla.iface interface
# definition file.
# The header files are copied to a temporary file apart from the section between a //++Autogenerated
# comment and a //--Autogenerated comment which is generated by the printHFile and printLexHFile
# functions. After the temporary file is created, it is copied back to the original file name.

import string
import sys
import os
import Face

def Contains(s,sub):
	return string.find(s, sub) != -1


def printMainFile(f,out):
	for name in f.order:
		v = f.features[name]
		if v["Category"] != "Deprecated":
			if v["FeatureType"] in ["fun", "get", "set"]:
				#featureDefineName = "SCI_" + string.upper(name)
				if v["Param1Type"] == "keymod" or v["Param2Type"] == "keymod":
					continue
				# don't include these!
				if not includeName(name):
					continue
				
				# TODO : fix these
				if name in ["GetStyledText", "AddStyledText"]:
					continue
				
				name = checkNameChange(name)
				
				# output the method
				if v.has_key("Comment"):
					out.write("\tRem\n")
					count = 0
					for comment in v["Comment"]:
						if count == 0:
							out.write("\tbbdoc: ")
						elif count == 1:
							out.write("\tabout: ")
						else:
							out.write("\t")
						out.write(comment + "\n")
						count = count + 1
					out.write("\tEnd Rem\n")
				
				out.write("\tMethod " + name)
				
				# special cases
				if name == "GetCurLine":
					out.write(":String(index:Int Var)\n")
					out.write("\t\tReturn bmx_wxscintilla_getcurline(wxObjectPtr, VarPtr index)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "FindText":
					out.write(":Int(minPos:Int, maxPos:Int, text:String, flags:Int)\n")
					out.write("\t\tReturn bmx_wxscintilla_findtext(wxObjectPtr, minPos, maxPos, text, flags)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "FormatRange":
					out.write(":Int(doDraw:Int, startPos:Int, endPos:Int, draw:wxDC, target:wxDC, renderRect:wxRect, pageRect:wxRect)\n")
					out.write("\t\tReturn bmx_wxscintilla_formatrange(wxObjectPtr, doDraw, startPos, endPos, draw.wxObjectPtr, target.wxObjectPtr, renderRect.wxObjectPtr, pageRect.wxObjectPtr)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "GetLine":
					out.write(":String(line:Int)\n")
					out.write("\t\tReturn bmx_wxscintilla_getline(wxObjectPtr, line)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "GetSelectedText":
					out.write(":String()\n")
					out.write("\t\tReturn bmx_wxscintilla_getselectedtext(wxObjectPtr)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "GetTextRange":
					out.write(":String(startPos:Int, endPos:Int)\n")
					out.write("\t\tReturn bmx_wxscintilla_gettextrange(wxObjectPtr, startPos, endPos)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "GetText":
					out.write(":String()\n")
					out.write("\t\tReturn bmx_wxscintilla_gettext(wxObjectPtr)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "GetProperty":
					out.write(":String(key:String)\n")
					out.write("\t\tReturn bmx_wxscintilla_getproperty(wxObjectPtr, key)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "GetPropertyExpanded":
					out.write(":String(key:String)\n")
					out.write("\t\tReturn bmx_wxscintilla_getpropertyexpanded(wxObjectPtr, key)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "MarkerDefineBitmap":
					out.write("(markerNumber:Int, bitmap:wxBitmap)\n")
					out.write("\t\tbmx_wxscintilla_markerdefinebitmap(wxObjectPtr, markerNumber, bitmap.wxObjectPtr)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "GetDocPointer":
					out.write(":Byte Ptr()\n")
					out.write("\t\tReturn bmx_wxscintilla_getdocpointer(wxObjectPtr)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "SetDocPointer":
					out.write("(docPointer:Byte Ptr)\n")
					out.write("\t\tbmx_wxscintilla_setdocpointer(wxObjectPtr, docPointer)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "ReleaseDocument":
					out.write("(docPointer:Byte Ptr)\n")
					out.write("\t\tbmx_wxscintilla_releasedocument(wxObjectPtr, docPointer)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "CreateDocument":
					out.write(":Byte Ptr()\n")
					out.write("\t\tReturn bmx_wxscintilla_createdocument(wxObjectPtr)\n")
					out.write("\tEnd Method\n\n")
					continue
				elif name == "AddRefDocument":
					out.write("(docPointer:Byte Ptr)\n")
					out.write("\t\tbmx_wxscintilla_addrefdocument(wxObjectPtr, docPointer)\n")
					out.write("\tEnd Method\n\n")
					continue
				
				if v["ReturnType"] != "void":
					rtype = "UNDEFINED"
					if v["ReturnType"] in ["int", "bool", "position"]:
						rtype = "Int"
					if v["ReturnType"] in ["colour"]:
						rtype = "wxColour"
					out.write(":" + rtype)
				out.write("(")
				if v["Param1Type"]:
					if v["Param1Type"] == "int" and v["Param1Name"] == "length" and v["Param2Type"] == "string":
						out.write(v["Param2Name"] + ":String)\n")
						out.write("\t\t")
						if v["ReturnType"] != "void":
							out.write("Return ")
						out.write("bmx_wxscintilla_" + string.lower(name))
						out.write("(wxObjectPtr, " + v["Param2Name"] + ")\n")
						out.write("\tEnd Method\n\n")
						continue
					else:
						paramName = v["Param1Name"]
						if paramName == "type":
							paramName = "type_"
						elif paramName == "handle":
							paramName = "handle_"
						elif paramName == "start":
							paramName = "startPos"
						elif paramName == "end":
							paramName = "endPos"
						out.write(paramName)
						if v["Param1Type"] in ["int", "position", "bool"]:
							 out.write(":Int")
						elif v["Param1Type"] in ["colour"]:
							out.write(":wxColour")
						elif v["Param1Type"] == "string":
							out.write(":String")
						else:
							out.write(", PARAM! - " + v["Param1Type"])
				if v["Param2Type"]:
					if v["Param1Type"]:
						out.write(", ")
					paramName = v["Param2Name"]
					if paramName == "type":
						paramName = "type_"
					elif paramName == "handle":
						paramName = "handle_"
					elif paramName == "start":
						paramName = "startPos"
					elif paramName == "end":
						paramName = "endPos"
					out.write(paramName)
					if v["Param2Type"] in ["int", "position", "bool"]:
						 out.write(":Int")
					elif v["Param2Type"] in ["colour"]:
						out.write(":wxColour")
					elif v["Param2Type"] == "string":
						out.write(":String")
					else:
						out.write(", PARAM! - " + v["Param2Type"])
				out.write(")\n")
				
				# The method content...
				out.write("\t\t")
				if v["ReturnType"] != "void":
					out.write("Return ")
				
				if v["ReturnType"] == "colour":
					out.write("wxColour._create(")
				
				out.write("bmx_wxscintilla_" + string.lower(name) + "(wxObjectPtr")
				if v["Param1Type"]:
					paramName = v["Param1Name"]
					if paramName == "type":
						paramName = "type_"
					elif paramName == "handle":
						paramName = "handle_"
					elif paramName == "start":
						paramName = "startPos"
					elif paramName == "end":
						paramName = "endPos"
					out.write(", " + paramName)
					
					if v["Param1Type"] == "colour":
						out.write(".wxObjectPtr")
				
				if v["Param2Type"]:
					paramName = v["Param2Name"]
					if paramName == "type":
						paramName = "type_"
					elif paramName == "handle":
						paramName = "handle_"
					elif paramName == "start":
						paramName = "startPos"
					elif paramName == "end":
						paramName = "endPos"
					out.write(", " + paramName)
					
					if v["Param2Type"] == "colour":
						out.write(".wxObjectPtr")
				
				
				out.write(")")
				
				if v["ReturnType"] == "colour":
					out.write(")")
				out.write("\n")
				
				# method end...
				out.write("\tEnd Method\n\n")


def printCommonFile(f,out):
	for name in f.order:
		v = f.features[name]
		if v["Category"] != "Deprecated":
			if v["FeatureType"] in ["fun", "get", "set"]:
				#featureDefineName = "SCI_" + string.upper(name)
				if v["Param1Type"] == "keymod" or v["Param2Type"] == "keymod":
					continue
				# don't include these!
				if not includeName(name):
					continue
				
				# TODO : fix these
				if name in ["GetStyledText", "AddStyledText"]:
					continue
				
				name = checkNameChange(name)
				
				# output the function
				out.write("\tFunction bmx_wxscintilla_" + string.lower(name))
				
				# special cases
				if name == "GetCurLine":
					out.write(":String(handle:Byte Ptr, index:Int Ptr)\n")
					continue
				elif name == "FindText":
					out.write(":Int(handle:Byte Ptr, minPos:Int, maxPos:Int, text:String, flags:Int)\n")
					continue
				elif name == "FormatRange":
					out.write(":Int(handle:Byte Ptr, doDraw:Int, startPos:Int, endPos:Int, draw:Byte Ptr, target:Byte Ptr, renderRect:Byte Ptr, pageRect:Byte Ptr)\n")
					continue
				elif name == "GetLine":
					out.write(":String(handle:Byte Ptr, line:Int)\n")
					continue
				elif name == "GetSelectedText":
					out.write(":String(handle:Byte Ptr)\n")
					continue
				elif name == "GetTextRange":
					out.write(":String(handle:Byte Ptr, startPos:Int, endPos:Int)\n")
					continue
				elif name == "GetText":
					out.write(":String(handle:Byte Ptr)\n")
					continue
				elif name == "GetProperty":
					out.write(":String(handle:Byte Ptr, key:String)\n")
					continue
				elif name == "GetPropertyExpanded":
					out.write(":String(handle:Byte Ptr, key:String)\n")
					continue
				elif name == "MarkerDefineBitmap":
					out.write("(handle:Byte Ptr, markerNumber:Int, bitmap:Byte Ptr)\n")
					continue
				elif name == "GetDocPointer":
					out.write(":Byte Ptr(handle:Byte Ptr)\n")
					continue
				elif name == "SetDocPointer":
					out.write("(handle:Byte Ptr, docPointer:Byte Ptr)\n")
					continue
				elif name == "ReleaseDocument":
					out.write("(handle:Byte Ptr, docPointer:Byte Ptr)\n")
					continue
				elif name == "CreateDocument":
					out.write(":Byte Ptr(handle:Byte Ptr)\n")
					continue
				elif name == "AddRefDocument":
					out.write("(handle:Byte Ptr, docPointer:Byte Ptr)\n")
					continue
				
				if v["ReturnType"] != "void":
					rtype = "UNDEFINED"
					if v["ReturnType"] in ["int", "bool", "position"]:
						rtype = "Int"
					if v["ReturnType"] in ["colour"]:
						rtype = "Byte Ptr"
					out.write(":" + rtype)
				out.write("(handle:Byte Ptr")
				if v["Param1Type"]:
					if v["Param1Type"] == "int" and v["Param1Name"] == "length" and v["Param2Type"] == "string":
						out.write(", " + v["Param2Name"] + ":String)\n")
						continue
					else:
						paramName = v["Param1Name"]
						if paramName == "type":
							paramName = "type_"
						elif paramName == "handle":
							paramName = "handle_"
						elif paramName == "start":
							paramName = "startPos"
						elif paramName == "end":
							paramName = "endPos"
						out.write(", " + paramName)
						if v["Param1Type"] in ["int", "position", "bool"]:
							 out.write(":Int")
						elif v["Param1Type"] in ["colour"]:
							out.write(":Byte Ptr")
						elif v["Param1Type"] == "string":
							out.write(":String")
						else:
							out.write(", PARAM! - " + v["Param1Type"])
				if v["Param2Type"]:
					paramName = v["Param2Name"]
					if paramName == "type":
						paramName = "type_"
					elif paramName == "handle":
						paramName = "handle_"
					elif paramName == "start":
						paramName = "startPos"
					elif paramName == "end":
						paramName = "endPos"
					out.write(", " + paramName)
					if v["Param2Type"] in ["int", "position", "bool"]:
						 out.write(":Int")
					elif v["Param2Type"] in ["colour"]:
						out.write(":Byte Ptr")
					elif v["Param2Type"] == "string":
						out.write(":String")
					else:
						out.write(", PARAM! - " + v["Param2Type"])
				out.write(")\n")
			#elif v["FeatureType"] in ["evt"]:
			#	featureDefineName = "SCN_" + string.upper(name)
			#	out.write("#define " + featureDefineName + " " + v["Value"] + "\n")
			#elif v["FeatureType"] in ["val"]:
			#	if not (Contains(name, "SCE_") or Contains(name, "SCLEX_")):
			#		out.write("#define " + name + " " + v["Value"] + "\n")


def printGlueHFile(f,out):
	for name in f.order:
		v = f.features[name]
		if v["Category"] != "Deprecated":
			if v["FeatureType"] in ["fun", "get", "set"]:
				#featureDefineName = "SCI_" + string.upper(name)
				if v["Param1Type"] == "keymod" or v["Param2Type"] == "keymod":
					continue
				# don't include these!
				if not includeName(name):
					continue
				
				# TODO : fix these
				if name in ["GetStyledText", "AddStyledText"]:
					continue
				
				name = checkNameChange(name)
				
				
				# special cases
				if name == "GetCurLine":
					out.write("\tBBString * bmx_wxscintilla_getcurline(wxScintilla * sc, int * index);\n")
					continue
				elif name == "FindText":
					out.write("\tint bmx_wxscintilla_findtext(wxScintilla * sc, int minPos, int maxPos, BBString * text, int flags);\n")
					continue
				elif name == "FormatRange":
					out.write("\tint bmx_wxscintilla_formatrange(wxScintilla * sc, bool doDraw, int start, int end, MaxDC * draw, MaxDC * target, MaxRect * renderRect, MaxRect * pageRect);\n")
					continue
				elif name == "GetLine":
					out.write("\tBBString * bmx_wxscintilla_getline(wxScintilla * sc, int line);\n")
					continue
				elif name == "GetSelectedText":
					out.write("\tBBString * bmx_wxscintilla_getselectedtext(wxScintilla * sc);\n")
					continue
				elif name == "GetTextRange":
					out.write("\tBBString * bmx_wxscintilla_gettextrange(wxScintilla * sc, int start, int end);\n")
					continue
				elif name == "GetText":
					out.write("\tBBString * bmx_wxscintilla_gettext(wxScintilla * sc);\n")
					continue
				elif name == "GetProperty":
					out.write("\tBBString * bmx_wxscintilla_getproperty(wxScintilla * sc, BBString * key);\n")
					continue
				elif name == "GetPropertyExpanded":
					out.write("\tBBString * bmx_wxscintilla_getpropertyexpanded(wxScintilla * sc, BBString * key);\n")
					continue
				elif name == "MarkerDefineBitmap":
					out.write("\tvoid bmx_wxscintilla_markerdefinebitmap(wxScintilla * sc, int markerNumber, MaxBitmap * bitmap);\n")
					continue
				elif name == "GetDocPointer":
					out.write("\tvoid * bmx_wxscintilla_getdocpointer(wxScintilla * sc);\n")
					continue
				elif name == "SetDocPointer":
					out.write("\tvoid bmx_wxscintilla_setdocpointer(wxScintilla * sc, void * docPointer);\n")
					continue
				elif name == "ReleaseDocument":
					out.write("void bmx_wxscintilla_releasedocument(wxScintilla * sc, void * docPointer);\n")
					continue
				elif name == "CreateDocument":
					out.write("void * bmx_wxscintilla_createdocument(wxScintilla * sc);\n")
					continue
				elif name == "AddRefDocument":
					out.write("void bmx_wxscintilla_addrefdocument(wxScintilla * sc, void * docPointer);\n")
					continue
				
				out.write("\t")
				if v["ReturnType"] in ["void", "int", "bool"]:
					out.write(v["ReturnType"])
				elif v["ReturnType"]  == "position":
					out.write("int")
				if v["ReturnType"] == "colour":
					out.write("MaxColour *")
				
				# output the function
				out.write(" bmx_wxscintilla_" + string.lower(name))
				
				out.write("(wxScintilla * sc")
				if v["Param1Type"]:
					if v["Param1Type"] == "int" and v["Param1Name"] == "length" and v["Param2Type"] == "string":
						out.write(", BBString * " + v["Param2Name"] + ");\n")
						continue
					else:
						out.write(", ")
						if v["Param1Type"] in ["int", "bool"]:
							 out.write(v["Param1Type"])
						elif v["Param1Type"] == "position":
							out.write("int")
						elif v["Param1Type"] in ["colour"]:
							out.write("MaxColour *")
						elif v["Param1Type"] == "string":
							out.write("BBString *")
						else:
							out.write(", PARAM! - " + v["Param1Type"])
						out.write(" " + v["Param1Name"])
				if v["Param2Type"]:
						out.write(", ")
						if v["Param2Type"] in ["int", "bool"]:
							 out.write(v["Param2Type"])
						elif v["Param2Type"] == "position":
							out.write("int")
						elif v["Param2Type"] in ["colour"]:
							out.write("MaxColour *")
						elif v["Param2Type"] == "string":
							out.write("BBString *")
						else:
							out.write(" PARAM! - " + v["Param2Type"])
						out.write(" " + v["Param2Name"])
				out.write(");\n")
			#elif v["FeatureType"] in ["evt"]:
			#	featureDefineName = "SCN_" + string.upper(name)
			#	out.write("#define " + featureDefineName + " " + v["Value"] + "\n")
			#elif v["FeatureType"] in ["val"]:
			#	if not (Contains(name, "SCE_") or Contains(name, "SCLEX_")):
			#		out.write("#define " + name + " " + v["Value"] + "\n")


def printGlueCPPFile(f,out):
	for name in f.order:
		v = f.features[name]
		if v["Category"] != "Deprecated":
			if v["FeatureType"] in ["fun", "get", "set"]:
				#featureDefineName = "SCI_" + string.upper(name)
				if v["Param1Type"] == "keymod" or v["Param2Type"] == "keymod":
					continue
				# don't include these!
				if not includeName(name):
					continue
				
				# TODO : fix these
				if name in ["GetStyledText", "AddStyledText"]:
					continue
				
				name = checkNameChange(name)
				
				# special cases
				if name == "GetCurLine":
					out.write("BBString * bmx_wxscintilla_getcurline(wxScintilla * sc, int * index) {\n")
					out.write("\treturn bbStringFromWxString(sc->GetCurLine(index));\n")
					out.write("}\n\n")
					continue
				elif name == "FindText":
					out.write("int bmx_wxscintilla_findtext(wxScintilla * sc, int minPos, int maxPos, BBString * text, int flags) {\n")
					out.write("\treturn sc->FindText(minPos, maxPos, wxStringFromBBString(text), flags);\n")
					out.write("}\n\n")
					continue
				elif name == "FormatRange":
					out.write("int bmx_wxscintilla_formatrange(wxScintilla * sc, bool doDraw, int start, int end, MaxDC * draw, MaxDC * target, MaxRect * renderRect, MaxRect * pageRect) {\n")
					out.write("\treturn sc->FormatRange(doDraw, start, end, draw->GetDC(), target->GetDC(), renderRect->Rect(), pageRect->Rect());\n")
					out.write("}\n\n")
					continue
				elif name == "GetLine":
					out.write("BBString * bmx_wxscintilla_getline(wxScintilla * sc, int line) {\n")
					out.write("\treturn bbStringFromWxString(sc->GetLine(line));\n")
					out.write("}\n\n")
					continue
				elif name == "GetSelectedText":
					out.write("BBString * bmx_wxscintilla_getselectedtext(wxScintilla * sc) {\n")
					out.write("\treturn bbStringFromWxString(sc->GetSelectedText());\n")
					out.write("}\n\n")
					continue
				elif name == "GetTextRange":
					out.write("BBString * bmx_wxscintilla_gettextrange(wxScintilla * sc, int start, int end) {\n")
					out.write("\treturn bbStringFromWxString(sc->GetTextRange(start, end));\n")
					out.write("}\n\n")
					continue
				elif name == "GetText":
					out.write("BBString * bmx_wxscintilla_gettext(wxScintilla * sc) {\n")
					out.write("\treturn bbStringFromWxString(sc->GetText());\n")
					out.write("}\n\n")
					continue
				elif name == "GetProperty":
					out.write("BBString * bmx_wxscintilla_getproperty(wxScintilla * sc, BBString * key) {\n")
					out.write("\treturn bbStringFromWxString(sc->GetProperty(wxStringFromBBString(key)));\n")
					out.write("}\n\n")
					continue
				elif name == "GetPropertyExpanded":
					out.write("BBString * bmx_wxscintilla_getpropertyexpanded(wxScintilla * sc, BBString * key) {\n")
					out.write("\treturn bbStringFromWxString(sc->GetPropertyExpanded(wxStringFromBBString(key)));\n")
					out.write("}\n\n")
					continue
				elif name == "PositionFromPoint":
					out.write("int bmx_wxscintilla_positionfrompoint(wxScintilla * sc, int x, int y) {\n")
					out.write("\treturn sc->PositionFromPoint(wxPoint(x, y));\n")
					out.write("}\n\n")
					continue
				elif name == "MarkerDefineBitmap":
					out.write("void bmx_wxscintilla_markerdefinebitmap(wxScintilla * sc, int markerNumber, MaxBitmap * bitmap) {\n")
					out.write("\tsc->MarkerDefineBitmap(markerNumber, bitmap->Bitmap());\n")
					out.write("}\n\n")
					continue
				elif name == "GetDocPointer":
					out.write("void * bmx_wxscintilla_getdocpointer(wxScintilla * sc) {\n")
					out.write("\treturn sc->GetDocPointer();\n")
					out.write("}\n\n")
					continue
				elif name == "SetDocPointer":
					out.write("void bmx_wxscintilla_setdocpointer(wxScintilla * sc, void * docPointer) {\n")
					out.write("\tsc->SetDocPointer(docPointer);\n")
					out.write("}\n\n")
					continue
				elif name == "ReleaseDocument":
					out.write("void bmx_wxscintilla_releasedocument(wxScintilla * sc, void * docPointer) {\n")
					out.write("\tsc->ReleaseDocument(docPointer);\n")
					out.write("}\n\n")
					continue
				elif name == "CreateDocument":
					out.write("void * bmx_wxscintilla_createdocument(wxScintilla * sc) {\n")
					out.write("\treturn sc->CreateDocument();\n")
					out.write("}\n\n")
					continue
				elif name == "AddRefDocument":
					out.write("void bmx_wxscintilla_addrefdocument(wxScintilla * sc, void * docPointer) {\n")
					out.write("\tsc->AddRefDocument(docPointer);\n")
					out.write("}\n\n")
					continue
			
				if v["ReturnType"] in ["void", "int", "bool"]:
					out.write(v["ReturnType"])
				elif v["ReturnType"]  == "position":
					out.write("int")
				if v["ReturnType"] == "colour":
					out.write("MaxColour *")
				
				# output the function
				out.write(" bmx_wxscintilla_" + string.lower(name))
				
				out.write("(wxScintilla * sc")
				if v["Param1Type"]:
					if v["Param1Type"] == "int" and v["Param1Name"] == "length" and v["Param2Type"] == "string":
						out.write(", BBString * " + v["Param2Name"] + ") {\n")
						out.write("\tsc->" + name + "(wxStringFromBBString(" + v["Param2Name"] + "));\n")
						out.write("}\n\n")
						continue
					else:
						out.write(", ")
						if v["Param1Type"] in ["int", "bool"]:
							 out.write(v["Param1Type"])
						elif v["Param1Type"] == "position":
							out.write("int")
						elif v["Param1Type"] in ["colour"]:
							out.write("MaxColour *")
						elif v["Param1Type"] == "string":
							out.write("BBString *")
						else:
							out.write(", PARAM! - " + v["Param1Type"])
						out.write(" " + v["Param1Name"])
				if v["Param2Type"]:
						out.write(", ")
						if v["Param2Type"] in ["int", "bool"]:
							 out.write(v["Param2Type"])
						elif v["Param2Type"] == "position":
							out.write("int")
						elif v["Param2Type"] in ["colour"]:
							out.write("MaxColour *")
						elif v["Param2Type"] == "string":
							out.write("BBString *")
						else:
							out.write(" PARAM! - " + v["Param2Type"])
						out.write(" " + v["Param2Name"])
				out.write(") {\n")
				
				# The method implementation section
				if v["ReturnType"] == "colour":
					out.write("\twxColour c(")
				elif v["ReturnType"] != "void":
					out.write("\treturn ")
				else:
					out.write("\t")

				if v["ReturnType"] == "string":
					out.write("bbStringFromWxString(")
				
				out.write("sc->" + name + "(")
				
				if v["Param1Type"]:
						if v["Param1Type"] in ["int", "bool", "position"]:
							 out.write(v["Param1Name"])
						elif v["Param1Type"] in ["colour"]:
							out.write(v["Param1Name"] + "->Colour()")
						elif v["Param1Type"] == "string":
							out.write("wxStringFromBBString(" + v["Param1Name"] + ")")
						else:
							out.write("PARAM! - " + v["Param1Type"])
				if v["Param2Type"]:
						if v["Param1Type"]:
							out.write(", ")
						if v["Param2Type"] in ["int", "bool", "position"]:
							 out.write(v["Param2Name"])
						elif v["Param2Type"] in ["colour"]:
							out.write(v["Param2Name"] + "->Colour()")
						elif v["Param2Type"] == "string":
							out.write("wxStringFromBBString(" + v["Param2Name"] + ")")
						else:
							out.write(" PARAM! - " + v["Param2Type"])
				
				out.write(")")
				
				if v["ReturnType"] in ["colour", "string"]:
					out.write(");\n")
				
				if v["ReturnType"] == "colour":
					out.write("\treturn new MaxColour(c);\n")
				else:
					out.write(";\n")
				
				# all done !
				out.write("}\n\n")
				
			#elif v["FeatureType"] in ["evt"]:
			#	featureDefineName = "SCN_" + string.upper(name)
			#	out.write("#define " + featureDefineName + " " + v["Value"] + "\n")
			#elif v["FeatureType"] in ["val"]:
			#	if not (Contains(name, "SCE_") or Contains(name, "SCLEX_")):
			#		out.write("#define " + name + " " + v["Value"] + "\n")

def printConstsFile(f,out):
	lastComment = ""
	for name in f.order:
		v = f.features[name]
		if v["Category"] != "Deprecated":
			#if v["FeatureType"] in ["fun", "get", "set"]:
			#	#featureDefineName = "SCI_" + string.upper(name)
			#	if v["Param1Type"] == "keymod" or v["Param2Type"] == "keymod":
			#		continue
			#	out.write("\t Function " + name)
			#	if v["ReturnType"] != "void":
			#		rtype = "UNDEFINED"
			#		if v["ReturnType"] in ["int", "bool", "position"]:
			#			rtype = "Int"
			#		if v["ReturnType"] in ["colour"]:
			#			rtype = "Byte Ptr"
			#		out.write(":" + rtype)
			#	out.write("(handle:Byte Ptr")
			#	if v["Param1Type"]:
			#		if v["Param1Type"] == "int" and v["Param1Name"] == "length" and v["Param2Type"] == "string":
			#			out.write(", " + v["Param2Name"] + ":String")
			#		else:
			#			if v["Param1Type"] in ["int", "position", "bool"]:
			#				out.write(", " + v["Param1Name"] + ":Int")
			#			elif v["Param1Type"] in ["colour"]:
			#				out.write(", " + v["Param1Name"] + ":Byte Ptr")
			#			elif v["Param1Type"] == "string":
			#				out.write(", " + v["Param1Name"] + ":String")
			#			else:
			#				out.write(", PARAM! - " + v["Param1Type"])
			#	out.write(")\n")
			#if v["FeatureType"] in ["evt"]:
			#	#featureDefineName = "SCN_" + string.upper(name)
			#	out.write("Const " + name + ":Int = " + v["Value"] + "\n")
			if v["FeatureType"] in ["val"]:
				if not Contains(name, "SCEN_"):
					if v.has_key("Comment"):
						if len(v["Comment"]) == 1:
							if lastComment != v["Comment"][0]:
								out.write("\n' " + v["Comment"][0] + "\n")
							lastComment = v["Comment"][0]
					convertName = name
					if convertName.startswith("SCE_"):
						convertName = convertName.replace("SCE_","wxSCI_")
					elif convertName.startswith("SC_"):
						convertName = convertName.replace("SC_","wxSCI_")
					elif convertName.startswith("SCFIND_"):
						convertName = convertName.replace("SCFIND_","wxSCI_")
					elif convertName.startswith("SCK_"):
						convertName = convertName.replace("SCK_","wxSCI_KEY_")
					elif convertName.startswith("INDIC"):
						convertName = convertName.replace("INDIC","wxSCI_INDIC")
					elif convertName.startswith("STYLE_"):
						convertName = convertName.replace("STYLE_","wxSCI_STYLE_")
					elif convertName.startswith("INVALID_"):
						convertName = convertName.replace("INVALID_","wxSCI_INVALID_")
					elif convertName.startswith("SCI_"):
						convertName = convertName.replace("SCI_","wxSCI_")
					elif convertName.startswith("SCWS_"):
						convertName = convertName.replace("SCWS_","wxSCI_WS_")
					elif convertName.startswith("EDGE_"):
						convertName = convertName.replace("EDGE_","wxSCI_EDGE_")
					elif convertName.startswith("SCLEX_"):
						convertName = convertName.replace("SCLEX_","wxSCI_LEX_")
					convertValue = v["Value"]
					if Contains(convertValue, "0x"):
						convertValue = convertValue.replace("0x", "$")
					out.write("Const " + convertName + ":Int = " + convertValue + "\n")

def CopyWithInsertion(input, output, genfn, definition):
	copying = 1
	for line in input.readlines():
		if copying:
			output.write(line)
		if Contains(line, "//++Autogenerated"):
			copying = 0
			genfn(definition, output)
		if Contains(line, "//--Autogenerated"):
			copying = 1
			output.write(line)

def contents(filename):
	f = file(filename)
	t = f.read()
	f.close()
	return t

def checkNameChange(name):
	if name == "GetSelText":
		name = "GetSelectedText"
	elif name == "SetSel":
		name = "SetSelection"
	elif name == "MarkerDefinePixmap":
		name = "MarkerDefineBitmap"
	elif name == "ScrollCaret":
		name = "EnsureCaretVisible"
	elif name == "ReplaceSel":
		name = "ReplaceSelection"
	elif name == "AssignCmdKey":
		name = "CmdKeyAssign"
	elif name == "ClearCmdKey":
		name = "CmdKeyClear"
	elif name == "ClearAllCmdKeys":
		name = "CmdKeyClearAll"
	elif name == "SetStylingEx":
		name = "SetStyleBytes"
	elif name == "CallTipPosStart":
		name = "CallTipPosAtStart"
	elif name.endswith("Fore"):
		name = name.replace("Fore", "Foreground")
	elif name.endswith("Back") and not Contains(name, "DeleteBack"):
		name = name.replace("Back", "Background")
	elif Contains(name, "WS"):
		name = name.replace("WS", "WhiteSpace")
	elif Contains(name, "MarginTypeN"):
		name = name.replace("MarginTypeN", "MarginType")
	elif Contains(name, "MarginWidthN"):
		name = name.replace("MarginWidthN", "MarginWidth")
	elif Contains(name, "MarginMaskN"):
		name = name.replace("MarginMaskN", "MarginMask")
	elif Contains(name, "MarginSensitiveN"):
		name = name.replace("MarginSensitiveN", "MarginSensitive")
	elif Contains(name, "AutoC"):
		name = name.replace("AutoC", "AutoComp")
	elif Contains(name, "Focus"):
		name = name.replace("Focus", "SCIFocus")
	elif Contains(name, "BackAlpha"):
		name = name.replace("BackAlpha", "BackgroundAlpha")
	elif Contains(name, "HScroll"):
		name = name.replace("HScroll", "UseHorizontalScroll")
	elif Contains(name, "VScroll"):
		name = name.replace("VScroll", "UseVerticalScroll")
	elif Contains(name, "ForeHlt"):
		name = name.replace("ForeHlt", "ForegroundHighlight")
	elif Contains(name, "Hlt"):
		name = name.replace("Hlt", "Highlight")
	
	if Contains(name, "Indic") and not Contains(name, "Indicator"):
		name = name.replace("Indic", "Indicator")
	
	return name

def includeName(name):
	if name in ["StyleGetFont", "EncodedFromUTF8", "TargetAsUTF8", "SetUsePalette", "StyleGetFore", "StyleGetBack", "StyleGetBold", "StyleGetItalic", "StyleGetSize", "StyleGetEOLFilled", "StyleGetUnderline", "StyleGetCase", "StyleGetCharacterSet", "StyleGetVisible", "StyleGetChangeable", "StyleGetHotSpot", "PointXFromPosition", "PointYFromPosition", "SetCaretStyle", "GetCaretStyle", "SetIndicatorCurrent", "GetIndicatorCurrent", "SetIndicatorValue", "GetIndicatorValue", "IndicatorFillRange", "IndicatorClearRange", "IndicatorAllOnFor", "IndicatorValueAt", "IndicatorStart", "IndicatorEnd", "GetPositionCache", "SetPositionCache", "LoadLexerLibrary", "SetLengthForEncode", "GetSelEOLFilled", "SetSelEOLFilled", "GetUsePalette", "GetDirectFunction", "GetDirectPointer", "IndicSetUnder", "IndicGetUnder", "Null", "GrabFocus", "CopyText", "GetCursor", "SetStylingEx", "SetCursor"]:
		return False
	if Contains(name, "GetHotspot"):
		return False
	return True

def Regenerate(filename, genfn, definition):
	inText = contents(filename)
	tempname = "MaxFacer.tmp"
	out = open(tempname,"w")
	hfile = open(filename)
	CopyWithInsertion(hfile, out, genfn, definition)
	out.close()
	hfile.close()
	outText = contents(tempname)
	if inText == outText:
		os.unlink(tempname)
	else:
		os.unlink(filename)
		os.rename(tempname, filename)

f = Face.Face()
try:
	f.ReadFromFile("src/scintilla/include/Scintilla.iface")
	Regenerate("wxscintilla.bmx", printMainFile, f)
	Regenerate("common.bmx", printCommonFile, f)
	Regenerate("consts.bmx", printConstsFile, f)
	Regenerate("glue.h", printGlueHFile, f)
	Regenerate("glue.cpp", printGlueCPPFile, f)
except:
	raise
