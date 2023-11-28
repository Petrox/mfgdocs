"""Classes supporting the display of steps and other resources from the model."""
from model import Step, Part
from storage import Storage


class ViewStep:
    """Methods related to viewing steps."""
    @staticmethod
    def find_steps_this_depends_on(step: Step, storage: Storage) -> dict[str, Step]:
        """Finds all steps that this step depends on.

        :param step: The step to find dependencies for.
        :param storage: The storage to use.
        :return: A dict of steps that this step depends on.
        """
        steps = {}
        for p in step.inputparts.keys():
            partkey, stepkey = Part.extract_stepkey(p)
            if stepkey is not None and stepkey != '':
                if stepkey in storage.cache_steps.data:
                    steps[stepkey] = storage.cache_steps.data[stepkey]
        for skey in step.start_after.keys():
            if skey in storage.cache_steps.data:
                steps[skey] = storage.cache_steps.data[skey]
        return steps

    @staticmethod
    def find_steps_after_start_with_this(step: Step, storage: Storage) -> dict[Step]:
        """Finds all steps that this step can be done after those start.

        :param step: The step to find dependencies for.
        :param storage: The storage to use.
        :return: A dict of steps that may run in parallel with this step
        """
        steps = {}
        for skey in step.start_after_start.keys():
            if skey in storage.cache_steps.data:
                steps[skey] = storage.cache_steps.data[skey]

        return steps

    @staticmethod
    def find_steps_which_start_after_this_starts(step: Step, storage: Storage) -> dict[Step]:
        """Finds all steps that this step can be done after those start.

        :param step: The step to find dependencies for.
        :param storage: The storage to use.
        :return: A dict of steps that may run in parallel with this step
        """
        steps = {}
        for k,v in storage.cache_steps.data.items():
            if v.start_after_start is not None:
                if step.key in v.start_after_start:
                    steps[k] = v
        return steps

    @staticmethod
    def find_steps_depending_on_this(step: Step, storage: Storage) -> dict[Step]:
        """Finds all steps that depend on our step.

        :param step: The step to find dependencies for.
        :param storage: The storage to use.
        :return: A dict of steps that this step depends on.
        """
        steps = {}
        for s in storage.cache_steps.data.values():
            if step.key in s.start_after:
                steps[s.key] = s
            else:
                for p in s.inputparts.keys():
                    partkey: str
                    partkey, stepkey = Part.extract_stepkey(p)
                    if stepkey is not None and stepkey != '':
                        if stepkey == step.key:
                            steps[s.key] = s
        return steps
