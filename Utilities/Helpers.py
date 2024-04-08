from __future__ import annotations

from discord    import HTTPException, Interaction, InteractionResponded, NotFound
################################################################################

__all__ = (
    "edit_message_helper",
    "dummy_response",
)

################################################################################
async def edit_message_helper(interaction: Interaction, *args, **kwargs) -> None:

    try:
        await interaction.message.edit(*args, **kwargs)
    except:
        try:
            await interaction.edit_original_response(*args, **kwargs)
        except:
            print("Edit Message Helper FAILED")

################################################################################
async def dummy_response(interaction: Interaction) -> None:

    try:
        await interaction.response.edit()
    except NotFound:
        try:
            await interaction.followup.edit()
        except NotFound:
            try:
                await interaction.response.send_message("** **", delete_after=0.1)
            except (InteractionResponded, HTTPException):
                pass

################################################################################
