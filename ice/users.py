
def locate_eligible_users(steam):
  # `eligible` in this context means "is valid to sync ROMs for".
  # We want to ignore the anonymous context, because there is no
  # reason to sync ROMs for it since you cant log in as them.
  is_user_context = lambda context: context.user_id != 'anonymous'
  return filter(is_user_context, steam_module.local_user_contexts(self.steam))
