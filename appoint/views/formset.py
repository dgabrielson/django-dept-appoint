"""
Some mixins for dealing with formsets.
"""
#######################################################################


class FormsetMixin(object):
    """
    A mixin that provides a way to show and handle a formset in a request.
    """

    formset_initial = {}
    formset_class = None
    formset_prefix = None
    success_url = None

    def get_formset_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.formset_initial.copy()

    def get_formset_prefix(self):
        """
        Returns the prefix to use for forms on this view
        """
        return self.formset_prefix

    def get_formset_class(self):
        """
        Returns the form class to use in this view
        """
        return self.formset_class

    def get_formset(self, formset_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            "initial": self.get_formset_initial(),
            "prefix": self.get_formset_prefix(),
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update({"data": self.request.POST, "files": self.request.FILES})
        return kwargs


#######################################################################


class ModelInlineFormsetMixin(FormsetMixin):
    """
    A mixin that provides a way to show and handle a modelform in a request.
    """

    def get_formset_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(ModelInlineFormsetMixin, self).get_formset_kwargs()
        kwargs.update({"instance": self.object})
        return kwargs

    def formset_valid(self, form, formset):
        """
        If the form is valid, save the associated model.
        """
        value = super(ModelInlineFormsetMixin, self).form_valid(form)
        formset.instance = self.object
        self.object_inlines = formset.save()
        return value


#######################################################################


class ProcessModelInlineFormsetMixin(ModelInlineFormsetMixin):
    """
    A mixin that renders a form and formset on GET and processes it on POST.
    """

    def get_context_data(self, *args, **kwargs):
        """
        Augment context with formset.
        """
        context = super(ProcessModelInlineFormsetMixin, self).get_context_data(
            *args, **kwargs
        )
        formset_class = self.get_formset_class()
        formset = self.get_form(formset_class)
        context["formset"] = formset
        return context

    def form_valid(self, form):
        formset_class = self.get_formset_class()
        formset = self.get_form(formset_class)
        if formset.is_valid():
            return self.formset_valid(form, formset)
        else:
            return self.formset_invalid(form, formset)


#######################################################################
