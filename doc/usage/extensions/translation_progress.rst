:mod:`sphinx.ext.translation_progress` -- Translation progress notifications
==============================================================================

.. module:: sphinx.ext.translation_progress
   :synopsis: Display translation progress information for multilingual projects.
.. moduleauthor:: Various contributors

.. versionadded:: 8.3

.. role:: code-py(code)
   :language: Python

This extension displays informational notes at the top of documents that contain
untranslated content, helping readers understand when they are viewing partially
translated documentation.

When enabled, this extension automatically inserts a note admonition at the 
beginning of documents that are not fully translated, informing readers about 
the current translation progress and encouraging contributions to improve the 
translation.

The extension works by leveraging Sphinx's existing internationalization 
infrastructure and only activates when translation classes are enabled.

Configuration
-------------

.. confval:: translation_progress_classes
   :type: :code-py:`bool | str`
   :default: :code-py:`False`

   This is a core Sphinx configuration value that must be enabled for the
   translation progress extension to work. When set to ``True``, Sphinx adds
   CSS classes to indicate translation status and calculates translation
   progress statistics.

   .. note::
      This configuration value is built into Sphinx core and is not specific
      to this extension. It enables translation progress tracking throughout
      Sphinx.

.. confval:: translation_progress_message
   :type: :code-py:`str | None`
   :default: :code-py:`None`

   Custom message template to display in the translation progress note.
   The message can include the following placeholders:

   - ``{progress}`` - Progress percentage (0-100)
   - ``{translated}`` - Number of translated elements
   - ``{total}`` - Total number of translatable elements

   If not specified, a default message is used::

      "This document is {progress}% translated. Some content may appear in the original language. Help us improve the translation!"

Example configuration
---------------------

To enable translation progress notifications in your Sphinx project:

.. code-block:: python
   :caption: conf.py

   # Enable the extension
   extensions = [
       'sphinx.ext.translation_progress',
       # ... other extensions
   ]

   # Required: Enable translation progress classes
   translation_progress_classes = True

   # Optional: Custom message
   translation_progress_message = (
       "⚠️ This page is {progress}% translated. "
       "Help us complete the translation!"
   )

   # Required for translations to work
   language = 'de'  # or your target language
   locale_dirs = ['locale']

Behavior
--------

The extension only displays notes on documents that meet all of the following criteria:

1. :confval:`translation_progress_classes` is enabled
2. The document contains translatable content
3. The document is not fully translated (contains untranslated elements)
4. The current builder is not the gettext builder

Documents that are fully translated or contain no translatable content will not
display the translation progress note.

Integration with other builders
-------------------------------

This extension is designed to work with HTML-based builders. It automatically
skips processing when using the gettext builder, which is used for generating
translation templates.

The extension respects Sphinx's translation infrastructure and will only operate
when proper internationalization is configured.

.. seealso::

   :doc:`/usage/advanced/intl`
      Sphinx's internationalization guide

   :confval:`translation_progress_classes`
      Core configuration for translation progress tracking