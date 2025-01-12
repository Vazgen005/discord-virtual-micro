from typing import Any, Callable, Dict, Optional

import discord
from discord.ext.commands.converter import Greedy
from discord.ext.commands.parameters import Parameter, Signature


def get_signature_parameters(
    function: Callable[..., Any],
    globalns: Dict[str, Any],
    /,
    *,
    skip_parameters: Optional[int] = None,
) -> Dict[str, Parameter]:
    signature = Signature.from_callable(function)
    params: Dict[str, Parameter] = {}
    cache: Dict[str, Any] = {}
    eval_annotation = discord.utils.evaluate_annotation
    required_params = 1 if skip_parameters is None else skip_parameters
    if len(signature.parameters) < required_params:
        raise TypeError(
            f"Command signature requires at least {required_params} parameter(s)"
        )

    iterator = iter(signature.parameters.items())
    for _ in range(0, required_params):
        next(iterator)

    for name, parameter in iterator:
        default = parameter.default
        if isinstance(default, Parameter):  # update from the default
            if default.annotation is not Parameter.empty:
                # There are a few cases to care about here.
                # x: TextChannel = commands.CurrentChannel
                # x = commands.CurrentChannel
                # In both of these cases, the default parameter has an explicit annotation
                # but in the second case it's only used as the fallback.
                if default._fallback:
                    if parameter.annotation is Parameter.empty:
                        parameter._annotation = default.annotation
                else:
                    parameter._annotation = default.annotation

            parameter._default = default.default
            parameter._description = default._description
            parameter._displayed_default = default._displayed_default

        annotation = parameter.annotation

        if annotation is None:
            params[name] = parameter.replace(annotation=type(None))
            continue

        annotation = eval_annotation(annotation, globalns, globalns, cache)
        if annotation is Greedy:
            raise TypeError("Unparameterized Greedy[...] is disallowed in signature.")

        params[name] = parameter.replace(annotation=annotation)

    return params
