"""reverse-engineer the values of a string based on a template"""


class ReverseTemplate:
    token_sep = ("{", "}")

    def __init__(self, template: str):
        """
        :param template: The template string to use when reversing strings to values.

        :raises ValueError: if there is a duplicated token in the template!
        """
        self.template: str = template
        self.tokens = []
        self.__get_full_token_cache = {}
        self.__get_str_after_last_token_cache = None
        self.__get_str_between_tokens_cache = {}
        self.__parse_template_tokens()

    def __parse_template_tokens(self):
        init_pos = 0

        while init_pos > -1:
            init_pos = self.template.find(self.token_sep[0], init_pos)
            if init_pos == -1:
                break

            end_pos = self.template.find(self.token_sep[1], init_pos)
            if end_pos > -1:
                token_name = self.template[init_pos + 1 : end_pos]
                init_pos = end_pos

                if token_name in self.tokens:
                    raise ValueError(f"The token {token_name} is duplicated!")

                self.tokens.append(token_name)

    def __get_full_token(self, token):
        if token not in self.__get_full_token_cache:
            self.__get_full_token_cache[token] = (
                self.token_sep[0] + token + self.token_sep[1]
            )

        # Simply returns the token as it is in the template
        return self.token_sep[0] + token + self.token_sep[1]

    def __get_str_after_last_token(self):
        if self.__get_str_after_last_token_cache is not None:
            return self.__get_str_after_last_token_cache

        full_token = self.__get_full_token(self.tokens[-1])

        last_token_ended_at = self.template.find(full_token) + len(full_token)

        self.__get_str_after_last_token_cache = self.template[last_token_ended_at:]

        return self.__get_str_after_last_token_cache

    def __get_str_between_tokens(self, t1: str, t2: str):
        cache_key = t1 + t2

        if cache_key in self.__get_str_between_tokens_cache:
            return self.__get_str_between_tokens_cache[cache_key]

        t1_at = self.template.find(t1)
        t2_at = self.template.find(t2)

        self.__get_str_between_tokens_cache[cache_key] = self.template[
            t1_at + len(t1) : t2_at
        ]
        return self.__get_str_between_tokens_cache[cache_key]

    def reverse(self, str_to_convert):
        if not self.tokens:
            return {}

        token_ind = 0
        values = {}
        value_at_pos = 0
        tokens_len = len(self.tokens)

        # The tokens should already be sorted by first to last refered to self.template
        for i in range(0, tokens_len):
            values[self.tokens[i]] = None

            token = self.__get_full_token(self.tokens[i])
            token_start_pos = self.template.find(token)

            if value_at_pos == 0 and token_start_pos > 0:
                # This means this token's value is not the first thing to appear in the string we are reversing.
                value_at_pos = token_start_pos

            if i < tokens_len - 1:
                next_token = self.__get_full_token(self.tokens[i + 1])
            else:
                next_token = None

            if i == tokens_len - 1:
                static_val = self.__get_str_after_last_token()
            elif next_token:
                static_val = self.__get_str_between_tokens(token, next_token)

            token_val_end_at = (
                str_to_convert.find(static_val, value_at_pos)
                if static_val
                else len(str_to_convert)
            )

            values[self.tokens[i]] = str_to_convert[value_at_pos:token_val_end_at]

            value_at_pos = token_val_end_at + len(static_val)
            token_ind += 1

        return values
