/*
  Copyright (c) 2007 Bruce A Henderson
 
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
  
  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
*/ 

#include "glue.h"

// ---------------------------------------------------------------------------------------

MaxMessageDialog::MaxMessageDialog(BBObject * handle, wxWindow * parent, const wxString& message,
		const wxString& caption, long style, int x, int y)
	: wxMessageDialog(parent, message, caption, style, wxPoint(x, y))
{
	wxbind(this, handle);
}

MaxMessageDialog::~MaxMessageDialog() {
	wxunbind(this);
}


// *********************************************


MaxMessageDialog * bmx_wxmessagedialog_create(BBObject * handle, wxWindow * parent, BBString * message,
		BBString * caption, long style, int x, int y) {
	return new MaxMessageDialog(handle, parent, wxStringFromBBString(message), wxStringFromBBString(caption), style, x, y);
}

int bmx_wxmessagedialog_showmodal(wxMessageDialog * dialog) {
	return dialog->ShowModal();
}