    # def _update_terrain_curriculum(self, env_ids):
    #     """
    #     Implements terrain curriculum such that an environment levels up only if
    #     its per-env tracking_lin_vel_x_history is full and exceeds a threshold.
    #     If it levels up, the history for that environment is cleared.

    #     Args:
    #         env_ids (List[int]): ids of environments being reset
    #     """
    #     if not self.init_done:
    #         return

    #     # Define your threshold for "successful" tracking in the X direction.
    #     level_up_threshold = 0.8 * self.reward_scales["tracking_lin_vel"] / self.dt
    #     # Get terrain name IDs for the provided env_ids.
    #     terrain_ids = self.env_terrain_names[env_ids]
    #     unique_terrain_ids = torch.unique(terrain_ids)
    #     for terrain_id in unique_terrain_ids:
    #         # Create a mask for environments belonging to this terrain type.
    #         terrain_mask = (terrain_ids == terrain_id)
    #         terrain_env_ids = env_ids[terrain_mask]

    #         # Only consider environments that have full tracking history.
    #         full_mask = self.tracking_lin_vel_x_history_full[terrain_env_ids]
    #         if torch.sum(full_mask) == 0:
    #             # If none of the envs in this terrain have a full history, skip updating.
    #             continue

    #         full_env_ids = terrain_env_ids[full_mask]
    #         # Compute the mean of the stored rewards for those envs.
    #         mean_lin_vel_x = torch.mean(self.tracking_lin_vel_x_history[full_env_ids]).item()

    #         # If the performance meets the threshold, update all environments in this terrain.
    #         if mean_lin_vel_x >= level_up_threshold:
    #             for env_id in terrain_env_ids:
    #                 # Increase level by 1, clamped at (max_terrain_level - 1).
    #                 self.terrain_levels[env_id] += 1
    #                 self.terrain_levels[env_id] = torch.clamp(
    #                     self.terrain_levels[env_id], 0, self.max_terrain_level - 1
    #                 )

    #                 # Update the environment origin for the new terrain level.
    #                 self.env_origins[env_id] = self.terrain_origins[
    #                     self.terrain_levels[env_id], self.terrain_types[env_id]
    #                 ]

    #                 # Clear this environment’s tracking history so it can "earn" the next level.
    #                 self.tracking_lin_vel_x_history[env_id, :] = 0.0
    #                 self.tracking_lin_vel_x_history_idx[env_id] = 0
    #                 self.tracking_lin_vel_x_history_full[env_id] = False
    

    # def _update_terrain_curriculum(self, env_ids):
    #     """
    #     Implements an efficient terrain curriculum update that adjusts levels
    #     based on a group metric. For each terrain type present in env_ids, if the
    #     mean tracking_lin_vel_x for those envs with full history exceeds a level-up
    #     threshold (0.8 * reward_scale/dt), their levels are incremented. Conversely,
    #     if the mean falls below a level-down threshold (0.6 * reward_scale/dt),
    #     their levels are decremented. Updates are applied only to environments in env_ids.
        
    #     Args:
    #         env_ids (List[int] or Tensor): ids of environments being reset.
    #     """
    #     if not self.init_done:
    #         return

    #     # Define thresholds for performance.
    #     level_up_threshold = 0.8 * self.reward_scales["tracking_lin_vel"] / self.dt
    #     level_down_threshold = 0.7 * self.reward_scales["tracking_lin_vel"] / self.dt

    #     # Get terrain ids for the provided env_ids.
    #     terrain_ids = self.env_terrain_names[env_ids]
    #     unique_terrain_ids = torch.unique(terrain_ids)

    #     for terrain_id in unique_terrain_ids:
    #         # Select indices within env_ids that belong to the current terrain.
    #         terrain_mask = (terrain_ids == terrain_id)
    #         terrain_env_ids = env_ids[terrain_mask]

    #         # Identify environments with full tracking history.
    #         full_mask = self.tracking_lin_vel_x_history_full[terrain_env_ids]
    #         if torch.sum(full_mask) == 0:
    #             continue

    #         full_env_ids = terrain_env_ids[full_mask]
    #         # Compute the mean tracking metric in a vectorized way.
    #         mean_lin_vel_x = self.tracking_lin_vel_x_history[full_env_ids].mean().item()

    #         # Determine level change based on performance.
    #         if mean_lin_vel_x >= level_up_threshold:
    #             delta = 1
    #         elif mean_lin_vel_x < level_down_threshold:
    #             delta = -1
    #         else:
    #             continue  # No change if performance is between thresholds.

    #         # Vectorized update: Adjust levels and clamp.
    #         self.terrain_levels[terrain_env_ids] += delta
    #         self.terrain_levels[terrain_env_ids] = torch.clamp(
    #             self.terrain_levels[terrain_env_ids],
    #             0, self.max_terrain_level - 1
    #         )

    #         # Update origins using advanced indexing.
    #         self.env_origins[terrain_env_ids] = self.terrain_origins[
    #             self.terrain_levels[terrain_env_ids], self.terrain_types[terrain_env_ids]
    #         ]

    #         # Clear the tracking history for these environments in one go.
    #         self.tracking_lin_vel_x_history[terrain_env_ids, :] = 0.0
    #         self.tracking_lin_vel_x_history_idx[terrain_env_ids] = 0
    #         self.tracking_lin_vel_x_history_full[terrain_env_ids] = False



    # def update_command_curriculum(self, env_ids):
    #     """ Implements a curriculum of increasing commands

    #     Args:
    #         env_ids (List[int]): ids of environments being reset
    #     """
    #     # If the tracking reward is above 80% of the maximum, increase the range of commands
    #     if torch.mean(self.episode_sums["tracking_lin_vel"][env_ids]) / self.max_episode_length > 0.8 * self.reward_scales["tracking_lin_vel"]:
    #         self.command_ranges["lin_vel_x"][0] = np.clip(self.command_ranges["lin_vel_x"][0] - 0.2, self.command_ranges["limit_vel_x"][0], 0.).item()
    #         self.command_ranges["lin_vel_x"][1] = np.clip(self.command_ranges["lin_vel_x"][1] + 0.2, 0., self.command_ranges["limit_vel_x"][1]).item()

    #         # Increase the range of commands for y
    #         self.command_ranges["lin_vel_y"][0] = np.clip(self.command_ranges["lin_vel_y"][0] - 0.2, self.command_ranges["limit_vel_y"][0], 0.).item()
    #         self.command_ranges["lin_vel_y"][1] = np.clip(self.command_ranges["lin_vel_y"][1] + 0.2, 0., self.command_ranges["limit_vel_y"][1]).item()
        
    #     if torch.mean(self.episode_sums["tracking_ang_vel"][env_ids]) / self.max_episode_length > 0.8 * self.reward_scales["tracking_ang_vel"]:
    #     # Increase the range of commands for yaw
    #         self.command_ranges["ang_vel_yaw"][0] = np.clip(self.command_ranges["ang_vel_yaw"][0] - 0.2, self.command_ranges["limit_vel_yaw"][0], 0.).item()
    #         self.command_ranges["ang_vel_yaw"][1] = np.clip(self.command_ranges["ang_vel_yaw"][1] + 0.2, 0., self.command_ranges["limit_vel_yaw"][1]).item()

