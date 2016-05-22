from iepy.preprocess.ner.base import BaseNERRunner as IEPYBaseNERRunner
from iepy.data.models import CHAR_MAX_LENGHT


class BaseNERRunner(IEPYBaseNERRunner):

    def build_occurrence(self, key, kind_name, alias, offset, offset_end):
        # Check len(key) because IEPY doesn't
        if len(key) > CHAR_MAX_LENGHT:
            key_ = key[:CHAR_MAX_LENGHT]
            print('Key "%s" reduced to "%s"' % (key, key_))
            key = key_
        o = super(BaseNERRunner, self).build_occurrence(key, kind_name, alias,
                                                        offset, offset_end)
        return o
