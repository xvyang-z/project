package main

import (
	"fmt"
	"github.com/google/uuid"
	"golang.org/x/sys/windows/registry"
	"math/rand"
	"os"
	"path/filepath"
)

func delete_file() error {

	// 获取用户的家目录路径
	homeDir, err := os.UserHomeDir()
	if err != nil {
		println(`get user home dir error`)
		return err
	}

	// 拼接完整路径
	PermanentDeviceId := filepath.Join(homeDir, "AppData/Roaming/JetBrains/PermanentDeviceId")
	PermanentUserId := filepath.Join(homeDir, "AppData/Roaming/JetBrains/PermanentUserId")

	err = os.Remove(PermanentDeviceId)
	if err != nil {
	}
	err = os.Remove(PermanentUserId)
	if err != nil {
	}
	return nil
}

func change_registry() error {
	u1, _ := uuid.NewRandom()
	u2, _ := uuid.NewRandom()

	device_id := fmt.Sprintf("%07d", rand.Intn(int(1e7))) + u1.String()
	user_id_on_machine := u2.String()

	// 路径：HKEY_CURRENT_USER\Software\JavaSoft\Prefs\jetbrains
	key, _, _ := registry.CreateKey(registry.CURRENT_USER, `Software\JavaSoft\Prefs\jetbrains`, registry.ALL_ACCESS)
	defer func(key registry.Key) {
		err := key.Close()
		if err != nil {
			println(`close error`)
		}
	}(key)

	err := key.SetStringValue(`device_id`, device_id)
	if err != nil {
		println(`write device id error`)
		return err
	}

	err = key.SetStringValue(`user_id_on_machine`, user_id_on_machine)
	if err != nil {
		println(`write user id error`)
		return err
	}

	return nil
}

func main() {

	err := delete_file()
	if err != nil {
		return
	}
	err = change_registry()
	if err != nil {
		return
	}

	println(`success`)
}
