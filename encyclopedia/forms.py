from tkinter import Widget
from turtle import title
from django import forms

class EntryCreatForm(forms.Form):
     title = forms.CharField()
     content = forms.CharField( 
         Widget = forms.Textarea()
     )
