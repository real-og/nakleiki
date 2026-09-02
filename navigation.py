async def push_state(state, state_name):
    data = await state.get_data()
    stack = data.get("navigation_stack", [])

    stack.append(state_name)

    await state.update_data(
        navigation_stack=stack
    )


async def pop_state(state):
    data = await state.get_data()
    stack = data.get("navigation_stack", [])

    if len(stack) < 2:
        return None

    # убираем текущее состояние
    stack.pop()

    # теперь верхнее — предыдущее
    previous_state = stack[-1]

    await state.update_data(
        navigation_stack=stack
    )

    return previous_state