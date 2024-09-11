from django import forms
from django.db import models

from .models import CrispyTestModel


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SampleForm(BaseForm):
    is_company = forms.CharField(
        label="company", required=False, widget=forms.CheckboxInput()
    )
    email = forms.EmailField(
        label="email",
        max_length=30,
        required=True,
        widget=forms.TextInput(),
        help_text="Insert your email",
    )
    password1 = forms.CharField(
        label="password", max_length=30, required=True, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="re-enter password",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(),
    )
    first_name = forms.CharField(
        label="first name", max_length=5, required=True, widget=forms.TextInput()
    )
    last_name = forms.CharField(
        label="last name", max_length=5, required=True, widget=forms.TextInput()
    )
    datetime_field = forms.SplitDateTimeField(
        label="date time", widget=forms.SplitDateTimeWidget()
    )

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get("password1", None)
        password2 = self.cleaned_data.get("password2", None)
        if not password1 and not password2 or password1 != password2:
            raise forms.ValidationError("Passwords dont match")

        return self.cleaned_data


class AllFieldsForm(forms.Form):
    # CharField: Text input
    char_field = forms.CharField(label="CharField")

    # EmailField: Email input
    email_field = forms.EmailField(label="EmailField")

    # IntegerField: Number input
    integer_field = forms.IntegerField(label="IntegerField")

    # FloatField: Float number input
    float_field = forms.FloatField(label="FloatField")

    # BooleanField: Checkbox input
    boolean_field = forms.BooleanField(label="BooleanField", required=False)

    # DateField: Date input
    date_field = forms.DateField(label="DateField")

    # TimeField: Time input
    time_field = forms.TimeField(label="TimeField")

    # DateTimeField: DateTime input
    datetime_field = forms.DateTimeField(label="DateTimeField")

    # ChoiceField: Drop-down list
    choice_field = forms.ChoiceField(
        label="ChoiceField",
        choices=[("option1", "Option 1"), ("option2", "Option 2")],
    )

    choice_radio_field = forms.ChoiceField(
        label="ChoiceRadioField",
        widget=forms.RadioSelect,
        choices=[("option1", "Option 1"), ("option2", "Option 2")],
    )

    # MultipleChoiceField: Multiple select
    multiple_choice_field = forms.MultipleChoiceField(
        label="MultipleChoiceField",
        choices=[("option1", "Option 1"), ("option2", "Option 2")],
    )

    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[("option1", "Option 1"), ("option2", "Option 2")],
    )

    # FileField: File upload
    file_field = forms.FileField(label="FileField", required=False)

    # ImageField: Image upload
    image_field = forms.ImageField(label="ImageField", required=False)

    # URLField: URL input
    url_field = forms.URLField(label="URLField")

    # RegexField: Input with regex validation
    regex_field = forms.RegexField(
        label="RegexField",
        regex=r"^\d{4}-\d{2}-\d{2}$",
        help_text="Enter a date in YYYY-MM-DD format",
    )

    # DecimalField: Decimal number input
    decimal_field = forms.DecimalField(
        label="DecimalField", max_digits=10, decimal_places=2
    )

    # DurationField: Duration input
    duration_field = forms.DurationField(label="DurationField")

    # Hidden input
    hidden_field = forms.CharField(
        widget=forms.HiddenInput(),
    )

    # Textarea widget
    textarea_field = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40}),
    )

    # Number input with custom widget
    number_input_field = forms.FloatField(
        widget=forms.NumberInput(attrs={"step": "any"}),
    )

    # Password input
    password_input_field = forms.CharField(
        widget=forms.PasswordInput(),
    )


class CheckboxesSampleForm(BaseForm):
    checkboxes = forms.MultipleChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1,),
        widget=forms.CheckboxSelectMultiple,
    )

    alphacheckboxes = forms.MultipleChoiceField(
        choices=(
            ("option_one", "Option one"),
            ("option_two", "Option two"),
            ("option_three", "Option three"),
        ),
        initial=("option_two", "option_three"),
        widget=forms.CheckboxSelectMultiple,
    )

    numeric_multiple_checkboxes = forms.MultipleChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1, 2),
        widget=forms.CheckboxSelectMultiple,
    )

    inline_radios = forms.ChoiceField(
        choices=(
            ("option_one", "Option one"),
            ("option_two", "Option two"),
        ),
        widget=forms.RadioSelect,
        initial="option_two",
    )


class SelectSampleForm(BaseForm):
    select = forms.ChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1,),
        widget=forms.Select,
    )


class SampleForm3(BaseModelForm):
    class Meta:
        model = CrispyTestModel
        fields = ["email", "password"]
        exclude = ["password"]


class SampleForm4(BaseModelForm):
    class Meta:
        """
        before Django1.6, one cannot use __all__ shortcut for fields
        without getting the following error:
        django.core.exceptions.FieldError: Unknown field(s) (a, l, _) specified for CrispyTestModel
        because obviously it casts the string to a set
        """

        model = CrispyTestModel
        fields = "__all__"  # eliminate RemovedInDjango18Warning


class SampleForm5(BaseForm):
    choices = [
        (1, 1),
        (2, 2),
        (1000, 1000),
    ]
    checkbox_select_multiple = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=choices
    )
    radio_select = forms.ChoiceField(widget=forms.RadioSelect, choices=choices)
    pk = forms.IntegerField()


class SampleFormWithMedia(BaseForm):
    class Media:
        css = {"all": ("test.css",)}
        js = ("test.js",)


class SampleFormWithMultiValueField(BaseForm):
    multi = forms.SplitDateTimeField()


class CrispyEmptyChoiceTestModel(models.Model):
    fruit = models.CharField(
        choices=[("apple", "Apple"), ("pear", "Pear")],
        null=True,
        blank=True,
        max_length=20,
    )


class SampleForm6(BaseModelForm):
    class Meta:
        """
        When allowing null=True in a model field,
        the corresponding field will have a choice
        for the empty value.

        When the form is initialized by an instance
        with initial value None, this choice should
        be selected.
        """

        model = CrispyEmptyChoiceTestModel
        fields = ["fruit"]
        widgets = {"fruit": forms.RadioSelect()}


class SampleForm7(BaseModelForm):
    is_company = forms.CharField(
        label="company", required=False, widget=forms.CheckboxInput()
    )
    password2 = forms.CharField(
        label="re-enter password",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = CrispyTestModel
        fields = ("email", "password", "password2")


class SampleForm8(BaseModelForm):
    is_company = forms.CharField(
        label="company", required=False, widget=forms.CheckboxInput()
    )
    password2 = forms.CharField(
        label="re-enter password",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = CrispyTestModel
        fields = ("email", "password2", "password")


class FakeFieldFile:
    """
    Quacks like a FieldFile (has a .url and string representation), but
    doesn't require us to care about storages etc.
    """

    url = "something"

    def __str__(self):
        return self.url


class FileForm(BaseForm):
    file_field = forms.FileField(widget=forms.FileInput)
    clearable_file = forms.FileField(
        widget=forms.ClearableFileInput, required=False, initial=FakeFieldFile()
    )


class AdvancedFileForm(BaseForm):
    file_field = forms.FileField(
        widget=forms.FileInput(attrs={"class": "my-custom-class"})
    )
    clearable_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": "my-custom-class"}),
        required=False,
        initial=FakeFieldFile(),
    )


class GroupedChoiceForm(BaseForm):
    choices = [
        (
            "Audio",
            [
                ("vinyl", "Vinyl"),
                ("cd", "CD"),
            ],
        ),
        (
            "Video",
            [
                ("vhs", "VHS Tape"),
                ("dvd", "DVD"),
            ],
        ),
        ("unknown", "Unknown"),
    ]
    checkbox_select_multiple = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=choices
    )
    radio = forms.MultipleChoiceField(widget=forms.RadioSelect, choices=choices)


class CustomRadioSelect(forms.RadioSelect):
    pass


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    pass


class SampleFormCustomWidgets(BaseForm):
    inline_radios = forms.ChoiceField(
        choices=(
            ("option_one", "Option one"),
            ("option_two", "Option two"),
        ),
        widget=CustomRadioSelect,
        initial="option_two",
    )

    checkboxes = forms.MultipleChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1,),
        widget=CustomCheckboxSelectMultiple,
    )
