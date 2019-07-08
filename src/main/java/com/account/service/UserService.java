package com.account.service;

import com.account.model.User;

public interface UserService {
    void save(User user);

    User findByUsername(String username);
}
