#!/usr/bin/env python3

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2022 Junu Kwon <junukwon7@gmail.com>

"""Umjunsik-lang v2 programming language definition."""

from cms.grading import Language


__all__ = ["Umlang2"]


class Umlang2(Language):
    """This defines the Umjunsik-lang programming language, interpreted with the
    standard Umjunsik-lang interpreter available in the system.

    Umjunsik-lang v2 standard

    """

    @property
    def name(self):
        """See Language.name."""
        return "Umjunsik-lang 2"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".umm"]

    @property
    def executable_extension(self):
        """See Language.executable_extension."""
        return ".umm"

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        if source_filenames[0] != executable_filename:
            return [["/bin/cp", source_filenames[0], executable_filename]]
        else:
            # We need at least one command to collect execution stats.
            return [["/bin/true"]]

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""
        args = args if args is not None else []
        return [["/usr/bin/umlang_runtime.py", "--source="+executable_filename]]
